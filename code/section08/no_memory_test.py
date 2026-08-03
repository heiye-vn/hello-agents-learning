from pathlib import Path
from dotenv import load_dotenv

from hello_agents import SimpleAgent, HelloAgentsLLM

load_dotenv(Path(__file__).parent / ".env")

# 第一次对话
# agent = SimpleAgent(name="学习助手", llm=HelloAgentsLLM())
# response1 = agent.run("我叫张三，正在学习Python，目前掌握了基础语法")
# print(response1)


# 第二次对话（新的会话，例如重启程序后重新创建Agent）
agent = SimpleAgent(name="学习助手", llm=HelloAgentsLLM())
response2 = agent.run("你还记得我的学习进度吗？")
print(response2)
