import re
from typing import Optional, List, Dict, Any
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message, ToolRegistry

DEFAULT_PROMPTS = {
    "initial": """
请根据以下要求完成任务:

任务: {task}

请提供一个完整、准确的回答。
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间:

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。
""",
    "refine": """
请根据反馈意见改进你的回答:

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。
""",
}


class Memory:
    """
    短期记忆模块，用于存储智能体的执行与反思轨迹
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        """向记忆中添加一条记录 ('execution' 或 'reflection')"""
        self.records.append({"type": record_type, "content": content})

    def get_last_execution(self) -> str:
        """获取最近一次的执行结果"""
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return ""


class MyReflectionAgent(ReflectionAgent):
    """
    重写的 Reflection Agent - 包含详细的思考和反思过程
    基于【初始尝试 -> 反思评估 -> 循环优化】范式实现
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_iterations: int = 3,
        custom_prompts: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            max_iterations=max_iterations,
        )
        self.max_iterations = max_iterations
        self.prompts = custom_prompts if custom_prompts else DEFAULT_PROMPTS
        self.memory = Memory()
        print(f"✅ {name} 初始化完成，最大迭代次数: {max_iterations}")

    def run(self, input_text: str, **kwargs) -> str:
        """
        运行 Reflection Agent

        Args:
            input_text: 任务描述
            **kwargs: 其他参数

        Returns:
            最终优化后的结果
        """
        print(f"\n🤖 {self.name} 开始处理任务: {input_text}")
        self.memory = Memory()

        # 1. 初始尝试
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.prompts["initial"].format(task=input_text)
        initial_result = self._get_llm_response(initial_prompt, **kwargs)
        self.memory.add_record("execution", initial_result)
        print(f"📝 初始回答:\n{initial_result}")

        # 2. 迭代循环：反思与优化
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思
            print("\n🔍 正在进行反思...")
            last_result = self.memory.get_last_execution()
            reflect_prompt = self.prompts["reflect"].format(
                task=input_text, content=last_result
            )
            feedback = self._get_llm_response(reflect_prompt, **kwargs)
            self.memory.add_record("reflection", feedback)
            print(f"🤔 反思反馈:\n{feedback}")

            # b. 检查是否需要停止
            if (
                "无需改进" in feedback
                or "no need for improvement" in feedback.lower()
            ):
                print("\n✅ 反思认为回答已无需改进，任务完成。")
                break

            # c. 优化
            print("\n✏️ 正在根据反馈进行优化...")
            refine_prompt = self.prompts["refine"].format(
                task=input_text, last_attempt=last_result, feedback=feedback
            )
            refined_result = self._get_llm_response(refine_prompt, **kwargs)
            self.memory.add_record("execution", refined_result)
            print(f"✨ 优化后的回答:\n{refined_result}")

        final_result = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n🎉 最终回答:\n{final_result}")

        # 保存对话历史
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_result, "assistant"))

        return final_result

    def _get_llm_response(self, prompt: str, **kwargs) -> str:
        """调用 LLM 获取响应文本"""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.llm.invoke(messages, **kwargs)
        return (
            response.content if hasattr(response, "content") else str(response)
        )
