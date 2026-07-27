import re
from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""
import json
import re
from typing import Optional, Tuple, Any


class StructuredParser:
    def parse_output(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析结构化输出，支持以下格式：
        1. JSON格式: {"thought": "...", "action": "..."}
        2. 键值对格式: thought: ...\naction: ...
        3. 原始正则格式（向后兼容）
        """
        # 尝试解析为JSON
        try:
            data = json.loads(text.strip())
            thought = data.get("thought")
            action = data.get("action")
            if thought is not None and action is not None:
                return str(thought), str(action)
        except json.JSONDecodeError:
            pass

        # 尝试结构化键值对
        lines = text.strip().split("\n")
        thought = None
        action = None

        for line in lines:
            if line.lower().startswith("thought:"):
                thought = line[8:].strip()
            elif line.lower().startswith("action:"):
                action = line[7:].strip()

        return thought, action

    def parse_action(self, action_text: str) -> Tuple[Optional[str], Optional[Any]]:
        """解析动作文本，支持多种格式"""
        if not action_text:
            return None, None

        # 尝试解析为JSON动作
        if action_text.startswith("{"):
            try:
                action_obj = json.loads(action_text)
                if isinstance(action_obj, dict):
                    action_name = action_obj.get("name")
                    action_input = action_obj.get("input", {})
                    return action_name, action_input
            except:
                pass

        # 支持旧格式: action_name[input]
        if "[" in action_text and "]" in action_text:
            # 处理嵌套括号
            parts = action_text.split("[", 1)
            action_name = parts[0].strip()
            action_input = parts[1].rstrip("]")
            return action_name, self._safe_parse_input(action_input)

        # 简单空格分隔格式
        parts = action_text.split(maxsplit=1)
        if len(parts) == 2:
            return parts[0], parts[1]

        return action_text, None

    def _safe_parse_input(self, input_str: str) -> Any:
        """安全解析输入字符串"""
        try:
            # 尝试作为JSON解析
            return json.loads(input_str)
        except:
            # 返回原始字符串
            return input_str


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
        self.parser = StructuredParser()  # 添加解析器实例

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")

            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc, question=question, history=history_str
            )

            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            if not response_text:
                print("错误：LLM未能返回有效响应。")
                break

            # 使用 StructuredParser 解析响应
            thought, action = self.parser.parse_output(response_text)

            if thought:
                print(f"🤔 思考: {thought}")
            if not action:
                print("警告：未能解析出有效的Action，流程终止。")
                break

            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = action.replace("Finish", "").strip("[] ").strip()
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            # 使用 StructuredParser 解析动作
            tool_name, tool_input = self.parser.parse_action(action)
            if not tool_name or tool_input is None:
                self.history.append("Observation: 无效的Action格式，请检查。")
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)

            # 根据工具输入类型进行处理
            if tool_function:
                if isinstance(tool_input, dict):
                    observation = tool_function(**tool_input)
                else:
                    observation = tool_function(tool_input)
            else:
                observation = f"错误：未找到名为 '{tool_name}' 的工具。"

            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        return (match.group(1), match.group(2)) if match else (None, None)

    def _parse_action_input(self, action_text: str):
        match = re.match(r"\w+\[(.*)\]", action_text, re.DOTALL)
        return match.group(1) if match else ""


if __name__ == "__main__":
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)
    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    agent.run(question)
