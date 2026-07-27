"""ReAct 智能体实现"""

from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search, current_time
import re

# 设计系统提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应，每轮回答必须同时包含 Thought 和 Action 两个字段:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`: 调用一个可用工具。
- `Finish[最终答案]`: 当你收集到足够的信息，能够回答用户的最终问题时，必须输出此命令。

现在，请开始解决以下问题：
Question: {question}
History: {history}
"""


"""
ReactAgent 的核心是一个循环，它不断地“格式化提示词 -> 调用LLM -> 执行动作 -> 整合结果”，
直到任务完成或达到最大步数限制
"""


class ReActAgent:
    def __init__(
        self,
        llm_client: HelloAgentsLLM,
        tool_executor: ToolExecutor,
        max_steps: int = 5,
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        """运行ReAct智能体来回答一个问题。"""

        self.history = []  # 每次运行时重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            # 1. 格式化提示词
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc, question=question, history=history_str
            )

            # 2. 调用 LLM 进行思考
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)

            if not response_text:
                print("错误:LLM未能返回有效响应。")
                break

            # 3. 解析 LLM 的输出
            thought, action = self._parse_output(response_text)

            if thought:
                print(f"🤔 思考: {thought}")

            if not action:
                # 兜底逻辑：如果 LLM 没有严格输出 Action 字段，但输出了最终文本，直接作为最终答案输出
                fallback_answer = response_text.strip()
                if thought and len(thought) > 0:
                    # 如果能解析出 Thought，且没有 Action，将思考/正文内容作为最终回答
                    fallback_answer = thought
                print(f"🎉 最终答案 (未严格遵循 Action 格式): {fallback_answer}")
                return fallback_answer

            # 4. 执行 Action
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束（使用 re.DOTALL 兼容多行答案）
                match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                final_answer = match.group(1) if match else action
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if tool_name is None or tool_input is None:
                self.history.append("Observation: 无效的Action格式，请检查。")
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")

            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                # 如果 tool_input 为空字符串，支持无参调用
                observation = (
                    tool_function(tool_input) if tool_input else tool_function()
                )

            print(f"👀 观察: {observation}")

            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束（真正达到最大步数才执行）
        print(f"已达到最大步数 ({self.max_steps} 步)，流程终止。")
        return None

    def _parse_output(self, text: str):
        """解析 LLM 的输出，提取 Thought 和 Action。"""
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析 Action 字符串，提取工具名称和输入"""
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None


if __name__ == "__main__":
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)
    tool_executor.registerTool("Current_Time", "获取当前时间的工具", current_time)
    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
    question = "截止到当前时间，华为最新的手机是哪一款？它的主要卖点是什么？"
    agent.run(question)
