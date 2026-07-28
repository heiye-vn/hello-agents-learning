from typing import List, Dict, Any, Optional
from llm_client import HelloAgentsLLM


class Memory:
    """
    记忆模块：存储智能体的执行记录和反思记录，用于构建历史轨迹。
    """

    def __init__(self):
        # 存储所有记录的列表，每条记录包含 type 和 content 两个字段
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        """
        向记忆中添加一条新记录。
        - record_type: 'execution'（执行/代码）或 'reflection'（反思/反馈）
        - content: 记录的具体内容
        """
        self.records.append({"type": record_type, "content": content})
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """
        将所有记忆记录格式化为文本轨迹，用于构建提示词上下文。
        """
        trajectory = ""
        for record in self.records:
            if record["type"] == "execution":
                trajectory += f"--- 上一轮尝试 (代码) ---\n{record['content']}\n\n"
            elif record["type"] == "reflection":
                trajectory += f"--- 评审员反馈 ---\n{record['content']}\n\n"
        return trajectory.strip()

    def get_last_execution(self) -> Optional[str]:
        """获取最近一次的执行结果（最新生成的代码）。"""
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return None

    def get_all_executions(self) -> List[str]:
        """获取所有执行/代码记录，用于收敛检测。"""
        return [r["content"] for r in self.records if r["type"] == "execution"]

    def get_all_reflections(self) -> List[str]:
        """获取所有反思/反馈记录，用于退化检测。"""
        return [r["content"] for r in self.records if r["type"] == "reflection"]


# 初始执行提示词：让 LLM 首次生成代码
INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。请根据以下要求，编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。

要求: {task}

请直接输出代码，不要包含任何额外的解释。
"""

# 反思提示词：让 LLM 评审代码并提出改进建议
REFLECT_PROMPT_TEMPLATE = """
你是一位极其严格的代码评审专家和资深算法工程师，对代码的性能有极致的要求。
你的任务是审查以下Python代码，并专注于找出其在**算法效率**上的主要瓶颈。

# 原始任务:
{task}

# 待审查的代码:
```python
{code}
```

请分析该代码的时间复杂度，并思考是否存在一种**算法上更优**的解决方案来显著提升性能。
如果存在，请清晰地指出当前算法的不足，并提出具体的、可行的改进算法建议（例如，使用筛法替代试除法）。
如果代码在算法层面已经达到最优，请明确说明代码已无需改进。

请直接输出你的反馈，不要包含任何额外的解释。
"""

# 终止判定提示词：让 LLM 结构化判断反馈是否认为代码已达最优
STOP_CHECK_PROMPT_TEMPLATE = """
判断以下反馈的核心结论是否认为代码已无需改进。

反馈:
{feedback}

请只回答一个词: STOP (表示无需改进) 或 CONTINUE (表示需要继续改进)。
"""

# 优化提示词：让 LLM 根据反馈改进代码
REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。你正在根据一位代码评审专家的反馈来优化你的代码。

# 原始任务:
{task}

# 你上一轮尝试的代码:
{last_code_attempt}

# 评审员的反馈:
{feedback}

请根据评审员的反馈，生成一个优化后的新版本代码。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。
请直接输出优化后的代码，不要包含任何额外的解释。
"""


class ReflectionSmartAgent:
    """
    智能反思智能体：在原始 ReflectionAgent 基础上，引入多重终止条件，
    包括语义判定、收敛检测和退化检测，避免无意义的迭代浪费。
    """

    def __init__(self, llm_client, max_iterations=5):
        self.llm_client = llm_client  # LLM 客户端
        self.memory = Memory()  # 记忆模块
        self.max_iterations = max_iterations  # 最大迭代次数（安全网）

    def run(self, task: str):
        """执行反思-优化循环，直到触发任一终止条件或达到最大迭代次数。"""
        print(f"\n--- 开始处理任务 ---\n任务: {task}")

        # === 第 1 步：初始执行 ===
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        initial_code = self._get_llm_response(initial_prompt)
        self.memory.add_record("execution", initial_code)

        # === 第 2 步：迭代循环（反思 + 检查 + 优化） ===
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思：评审当前代码
            print("\n-> 正在进行反思...")
            last_code = self.memory.get_last_execution()
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=task, code=last_code)
            feedback = self._get_llm_response(reflect_prompt)
            self.memory.add_record("reflection", feedback)

            # b. 终止条件检查 1：语义判定
            #    让 LLM 理解反馈语义，判断是否认为代码已无需改进
            stop_decision = self._check_should_stop(feedback)
            if stop_decision == "STOP":
                print("\n✅ [语义判定] LLM 认为代码已无需改进，任务完成。")
                break

            # c. 终止条件检查 2：收敛检测
            #    如果连续两轮生成的代码完全相同，说明迭代已收敛
            if self._is_code_converged():
                print("\n✅ [收敛检测] 连续两轮代码完全相同，判定已收敛，任务完成。")
                break

            # d. 终止条件检查 3：反馈退化检测
            #    如果评审员的反馈内容开始重复，说明无法提出新建议
            if self._is_feedback_degrading():
                print("\n✅ [退化检测] 反馈内容正在重复/退化，再迭代无意义，任务完成。")
                break

            # e. 优化：根据反馈改进代码
            print("\n-> 正在进行优化...")
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=task, last_code_attempt=last_code, feedback=feedback
            )
            refined_code = self._get_llm_response(refine_prompt)
            self.memory.add_record("execution", refined_code)

        # 输出最终生成的代码
        final_code = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终生成的代码:\n{final_code}")
        return final_code

    def _check_should_stop(self, feedback: str) -> str:
        """
        语义判定：让 LLM 判断反馈的核心结论是否为"无需改进"。
        相比原始的关键词匹配，此方法能理解语义变化，鲁棒性更强。
        """
        prompt = STOP_CHECK_PROMPT_TEMPLATE.format(feedback=feedback)
        response = self._get_llm_response(prompt)
        response_clean = response.strip().upper()
        # 兜底：只有当明确出现 STOP 且没有 CONTINUE 时才终止
        if "STOP" in response_clean and "CONTINUE" not in response_clean:
            return "STOP"
        return "CONTINUE"

    def _is_code_converged(self) -> bool:
        """
        收敛检测：比较最近两次生成的代码是否完全相同。
        如果代码不再变化，说明 LLM 已找不到改进空间。
        零额外 LLM 调用成本。
        """
        executions = self.memory.get_all_executions()
        if len(executions) < 2:
            return False
        return executions[-1] == executions[-2]

    def _is_feedback_degrading(self) -> bool:
        """
        退化检测：比较最近两次反思反馈是否完全相同。
        如果反馈开始重复，说明评审员已无法提出新建议。
        零额外 LLM 调用成本。
        """
        reflections = self.memory.get_all_reflections()
        if len(reflections) < 2:
            return False
        return reflections[-1] == reflections[-2]

    def _get_llm_response(self, prompt: str) -> str:
        """调用 LLM 获取流式响应，失败时返回空字符串。"""
        messages = [{"role": "user", "content": prompt}]
        response_text = self.llm_client.think(messages=messages) or ""
        return response_text


if __name__ == "__main__":
    try:
        llm_client = HelloAgentsLLM()
    except Exception as e:
        print(f"初始化LLM客户端时出错: {e}")
        exit()

    # 创建智能反思智能体，最大迭代 5 轮
    agent = ReflectionSmartAgent(llm_client, max_iterations=5)
    task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"
    agent.run(task)
