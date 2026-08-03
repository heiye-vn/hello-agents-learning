import ast
import re
from typing import Optional, List, Dict, Any
from hello_agents import PlanSolveAgent, HelloAgentsLLM, Config, Message

# --- 规划器与执行器 Prompt 模板 ---
PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""


class Planner:
    """规划器：负责将问题分解为有序的执行计划步骤"""

    def __init__(self, llm_client: HelloAgentsLLM, prompt_template: Optional[str] = None):
        self.llm_client = llm_client
        self.prompt_template = prompt_template or PLANNER_PROMPT_TEMPLATE

    def plan(self, question: str, **kwargs) -> List[str]:
        """根据用户问题生成行动计划步骤列表"""
        prompt = self.prompt_template.format(question=question)
        messages = [{"role": "user", "content": prompt}]

        print("--- 正在生成计划 ---")
        response = self.llm_client.invoke(messages, **kwargs)
        response_text = (
            response.content if hasattr(response, "content") else str(response)
        ) or ""

        print(f"✅ 计划已生成:\n{response_text}")

        # 解析LLM输出的列表字符串
        try:
            if "```python" in response_text:
                plan_str = response_text.split("```python")[1].split("```")[0].strip()
            elif "```" in response_text:
                plan_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                plan_str = response_text.strip()

            plan = ast.literal_eval(plan_str)
            if isinstance(plan, list):
                return [str(item) for item in plan]
            return []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


class Executor:
    """执行器：按照计划一步步解决问题"""

    def __init__(self, llm_client: HelloAgentsLLM, prompt_template: Optional[str] = None):
        self.llm_client = llm_client
        self.prompt_template = prompt_template or EXECUTOR_PROMPT_TEMPLATE

    def execute(self, question: str, plan: List[str], **kwargs) -> str:
        """根据计划，逐步执行并解决问题"""
        history = ""
        final_answer = ""

        print("\n--- 正在执行计划 ---")

        for i, step in enumerate(plan, 1):
            print(f"\n-> 正在执行步骤 {i}/{len(plan)}: {step}")
            prompt = self.prompt_template.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step,
            )
            messages = [{"role": "user", "content": prompt}]

            response = self.llm_client.invoke(messages, **kwargs)
            response_text = (
                response.content if hasattr(response, "content") else str(response)
            ) or ""

            # 更新历史记录
            history += f"步骤 {i}: {step}\n结果: {response_text}\n\n"
            final_answer = response_text
            print(f"✅ 步骤 {i} 已完成，结果: {final_answer}")

        return final_answer


class MyPlanSolveAgent(PlanSolveAgent):
    """
    重写的 Plan-and-Solve Agent - 先规划后执行的智能体范式
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        planner_prompt: Optional[str] = None,
        executor_prompt: Optional[str] = None,
    ):
        super().__init__(name=name, llm=llm, system_prompt=system_prompt, config=config)
        self.planner = Planner(self.llm, planner_prompt)
        self.executor = Executor(self.llm, executor_prompt)
        print(f"✅ {name} 初始化完成 (Plan-and-Solve 范式)")

    def run(self, input_text: str, **kwargs) -> str:
        """
        运行 Plan-and-Solve Agent

        Args:
            input_text: 要解决的问题
            **kwargs: 其他参数

        Returns:
            最终解决方案
        """
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        # 1. 生成计划
        plan = self.planner.plan(input_text, **kwargs)
        if not plan:
            final_answer = "无法生成有效的行动计划，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "assistant"))
            return final_answer

        # 2. 执行计划
        final_answer = self.executor.execute(input_text, plan, **kwargs)
        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")

        # 保存对话历史
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))

        return final_answer


# 提供别名以保证与不同习惯的类名调用兼容
MyPlanAndSolveAgent = MyPlanSolveAgent
