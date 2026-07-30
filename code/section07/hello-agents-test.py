import os
from pathlib import Path
from dotenv import load_dotenv

from hello_agents import SimpleAgent, HelloAgentsLLM

load_dotenv(Path(__file__).parent / ".env")

# 创建LLM实例 - 框架自动检测provider
llm = HelloAgentsLLM()

# 或手动指定provider（可选）
# llm = HelloAgentsLLM(provider="modelscope")

# 创建SimpleAgent
agent = SimpleAgent(name="AI助手", llm=llm, system_prompt="你是一个有用的AI助手")

# 基础对话
response = agent.run("你好，请介绍一下自己")
print(response)


# 添加工具功能（可选）
from hello_agents.tools import CalculatorTool

calculator = CalculatorTool()
agent.add_tool(calculator)

response = agent.run("帮我计算 2 + 3 * 4 是多少")
print(response)

# 查看对话历史
print(agent.get_history())
