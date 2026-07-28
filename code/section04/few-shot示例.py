import re
from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search

# 改进后的REACT_PROMPT_TEMPLATE，包含few-shot示例
REACT_PROMPT_TEMPLATE = """
你是一个有能力调用外部工具的智能助手。请严格按照以下格式进行回应：

可用工具如下：
{tools}

格式说明：
1. 首先进行`Thought:`，描述你的思考过程
2. 然后执行`Action:`，调用工具或输出最终答案
3. Action必须严格按照以下格式之一：
   - `{{工具名称}}[{{工具输入}}]`：调用工具
   - `Finish[最终答案]`：输出最终答案

示例1：
Thought: 用户询问北京今天的天气，我需要搜索天气信息。
Action: Search[北京今天天气]

示例2：
Thought: 用户询问计算数学表达式，我需要使用计算器工具。
Action: Calculator[(15 + 7) * 3 - 12]

示例3：
Thought: 我已经通过搜索获得了华为手机的信息，现在可以回答用户的问题了。
Action: Finish[华为最新手机是Mate 60 Pro，主要卖点是支持5G网络和卫星通信。]

示例4：
Thought: 用户询问了多个问题，我需要分步骤处理。首先搜索最新CPU信息。
Action: Search[2025年英特尔最新CPU型号]

示例5：
Thought: 搜索结果显示了CPU信息，但用户还询问了价格，需要进一步搜索价格信息。
Action: Search[英特尔酷睿i9-14900K价格]

示例6：
Thought: 现在我有足够的信息回答用户的所有问题了。
Action: Finish[英特尔最新CPU是酷睿i9-14900K，价格大约在5000-6000元人民币。]

请严格按照上述格式回应，不要输出任何额外内容。

现在，请开始解决以下问题：
Question: {question}
History: {history}
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

            thought, action = self._parse_output(response_text)
            if thought:
                print(f"🤔 思考: {thought}")
            if not action:
                print("警告：未能解析出有效的Action，流程终止。")
                break

            if action.startswith("Finish"):
                final_answer = self._parse_action_input(action)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                self.history.append("Observation: 无效的Action格式，请检查。")
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)
            observation = (
                tool_function(tool_input)
                if tool_function
                else f"错误：未找到名为 '{tool_name}' 的工具。"
            )

            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
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


def test_with_fewshot_examples():
    """测试few-shot示例的效果"""
    from llm_client import HelloAgentsLLM
    from tools import ToolExecutor, search, calculator

    # 初始化工具执行器
    tool_executor = ToolExecutor()
    tool_executor.registerTool(
        "Search",
        "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。",
        search,
    )
    tool_executor.registerTool(
        "Calculator",
        "一个数学计算器。能够计算复杂的数学表达式，支持加减乘除、括号、幂运算等。",
        calculator,
    )

    # 初始化LLM
    llm = HelloAgentsLLM()

    # 测试问题
    test_questions = [
        "华为最新的手机是哪一款？它的主要卖点是什么？",
        "计算一下(123 + 456) × 789 ÷ 12等于多少？",
        "特斯拉最新款电动车是什么？价格大概多少？",
        "2025年最流行的编程语言是什么？",
    ]

    print("=" * 60)
    print("Few-shot示例效果对比测试")
    print("=" * 60)

    for i, question in enumerate(test_questions, 1):
        print(f"\n测试 {i}: {question}")
        print("-" * 40)

        agent = ReActAgent(llm_client=llm, tool_executor=tool_executor, max_steps=3)
        result = agent.run(question)

        if result:
            print(f"✅ 测试完成: {result[:100]}...")
        else:
            print("❌ 测试失败或未完成")


if __name__ == "__main__":
    # 原有的主程序
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)

    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)

    # 测试示例问题
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    print("=" * 60)
    print("原问题测试:")
    print("=" * 60)
    agent.run(question)

    # 运行few-shot测试
    test_with_fewshot_examples()
