import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, ToolRegistry


import json
import urllib.request

from my_react_agent import MyReActAgent

load_dotenv(Path(__file__).parent / ".env")


def tavily_search(query: str) -> str:
    """使用 Tavily API 进行互联网搜索"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误：未在 .env 中找到 TAVILY_API_KEY 环境变量"

    url = "https://api.tavily.com/search"
    payload = json.dumps(
        {"api_key": api_key, "query": query, "search_depth": "basic", "max_results": 3}
    ).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            results = res_data.get("results", [])
            if not results:
                return "未搜索到相关信息。"

            output = []
            for item in results:
                title = item.get("title", "")
                content = item.get("content", "")
                output.append(f"【{title}】\n{content}")
            return "\n\n".join(output)
    except Exception as e:
        return f"搜索请求失败: {e}"


def test_react_agent():
    """测试 MyReactAgent 功能"""

    # 创建 LLM 实例
    llm = HelloAgentsLLM()

    # 创建工具注册表
    tool_registry = ToolRegistry()

    # 注册计算器工具
    try:
        from hello_agents import calculate

        tool_registry.register_function(
            "calculate", "执行数学计算，支持基本的四则运算", calculate
        )
        print("✅ 计算器工具注册成功")
    except ImportError:
        print("⚠️ 计算器工具未找到，跳过注册")

        # 注册搜索工具（如果可用）
    try:
        from hello_agents import search

        tool_registry.register_function("search", "搜索互联网信息", search)
        print("✅ 搜索工具注册成功")
    except ImportError:
        print("⚠️ 搜索工具未找到，跳过注册")

    # 注册 Tavily 搜索工具
    tool_registry.register_function(
        "search", "搜索互联网关于时事、事实或信息的工具", tavily_search
    )
    print("✅ Tavily 搜索工具注册成功")

    # 创建自定义 ReactAgent
    agent = MyReActAgent(
        name="我的推理行动助手", llm=llm, tool_registry=tool_registry, max_steps=5
    )

    print("\n" + "=" * 60)
    print("开始测试 MyReActAgent")
    print("=" * 60)

    # 测试1：数学计算问题
    print("\n📊 测试1：数学计算问题")
    math_question = "请帮我计算：(25 + 15) * 3 - 8 的结果是多少？"

    try:
        result1 = agent.run(math_question)
        print(f"\n🎯 测试1结果: {result1}")
    except Exception as e:
        print(f"❌ 测试1失败: {e}")

    # 测试2：需要搜索的问题
    print("\n🔍 测试2：信息搜索问题")
    search_question = "Python编程语言是什么时候发布的？请告诉我具体的年份。"

    try:
        result2 = agent.run(search_question)
        print(f"\n🎯 测试2结果: {result2}")
    except Exception as e:
        print(f"❌ 测试2失败: {e}")

    # 测试3：复合问题（需要多步推理）
    print("\n🧠 测试3：复合推理问题")
    complex_question = "如果一个班级有30个学生，其中60%是女生，那么男生有多少人？请先计算女生人数，再计算男生人数。"

    try:
        result3 = agent.run(complex_question)
        print(f"\n🎯 测试3结果: {result3}")
    except Exception as e:
        print(f"❌ 测试3失败: {e}")

    # 显示对话历史记录
    # print(f"\n📝 对话历史记录: {len(agent.get_history())} 条消息")

    # 显示工具使用统计
    print(f"\n🛠️ 可用工具数量: {len(tool_registry._tools)}")
    print("已注册的工具:")
    for tool_name in tool_registry._tools.keys():
        print(f"  - {tool_name}")

    print("\n🎉 测试完成！")


def test_custom_prompt():
    """测试自定义提示词的ReActAgent"""
    print("\n" + "=" * 60)
    print("测试自定义提示词的 MyReActAgent")
    print("=" * 60)

    # 创建LLM和工具注册表
    llm = HelloAgentsLLM()
    tool_registry = ToolRegistry()

    # 注册计算器工具
    try:
        from hello_agents import calculate

        tool_registry.register_function(
            "calculate", "数学计算，支持基本四则运算", calculate
        )
    except ImportError:
        pass

    # 自定义提示词（更简洁的版本）
    custom_prompt = """你是一个数学专家AI助手。

可用工具：{tools}

请按以下格式回应：
Thought: [你的思考]
Action: [tool_name[input] 或 Finish[答案]]

问题：{question}
历史：{history}

开始："""

    # 创建使用自定义提示词的Agent
    custom_agent = MyReActAgent(
        name="数学专家助手",
        llm=llm,
        tool_registry=tool_registry,
        max_steps=3,
        custom_prompt=custom_prompt,
    )

    # 测试数学问题
    math_question = "计算 15 × 8 + 32 ÷ 4 的结果"

    try:
        result = custom_agent.run(math_question)
        print(f"\n🎯 自定义提示词测试结果: {result}")
    except Exception as e:
        print(f"❌ 自定义提示词测试失败: {e}")


if __name__ == "__main__":
    # 运行基础测试（包含数学计算、Tavily 搜索和复合推理测试）
    test_react_agent()

    # 运行自定义提示词测试
    test_custom_prompt()

    print("\n✨ 所有测试完成！")
