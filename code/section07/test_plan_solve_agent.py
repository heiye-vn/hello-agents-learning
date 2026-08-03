import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from my_plan_solve_agent import MyPlanAndSolveAgent, MyPlanSolveAgent

load_dotenv(Path(__file__).parent / ".env")


def test_plan_solve_agent():
    """测试 MyPlanSolveAgent 功能"""
    # 创建 LLM 实例
    llm = HelloAgentsLLM()

    # 创建自定义 PlanAndSolveAgent
    agent = MyPlanAndSolveAgent(name="我的规划执行助手", llm=llm)

    # 测试复杂问题
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"

    print("\n" + "=" * 60)
    print("开始测试 MyPlanSolveAgent")
    print("=" * 60)

    result = agent.run(question)
    print(f"\n🎯 最终结果: {result}")

    # 查看对话历史
    print(f"\n📝 对话历史: {len(agent.get_history())} 条消息")
    print("🎉 测试完成！")


if __name__ == "__main__":
    test_plan_solve_agent()
