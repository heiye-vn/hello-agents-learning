import os
import asyncio

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import BaseChatMessage

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    model_info={
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "vision": False,
        "family": "unknown",
    },
)


def create_dialogue_monitor(model_client):
    return AssistantAgent(
        name="DialogueMonitor",
        model_client=model_client,
        system_message="""
你是对话质量监控器。

职责（非常重要）：
- 不要参与任务执行
- 不要写代码
- 不要提建议

每轮对话结束后，请根据对话历史判断是否出现以下**严格异常**：

1. 两名 Agent 来回重复同一句话超过 3 次（完全相同的发言）
2. 严重偏离用户原始需求，并且无法挽回
3. 出现无意义空转（Agent 之间只是互相问候、闲聊，完全不推进任务）

以下情况属于**正常对话，不算异常**：
- Agent 之间正常的讨论、改进建议、代码审查意见
- 工程师修改代码、审查员提出修改意见
- 来回沟通但不重复完全相同内容

如果正常：
→ 只说一行：DIALOGUE_OK

如果异常：
→ 只说一行：DIALOGUE_ANOMALY: <简要原因>
""",
    )


def create_product_manager():
    return AssistantAgent(
        name="ProductManager",
        model_client=model_client,
        system_message="""
你是产品经理。

职责：
1. 分析用户需求
2. 输出技术方案和验收标准
3. 说："请工程师开始实现"

回退规则：
- 如果工程师或审查员指出需求不合理，请重新分析并修改
""",
    )


def create_engineer():
    return AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message="""
你是资深 Python 工程师。

职责：
1. 根据需求编写完整可运行代码
2. 说："请代码审查员检查"

回退规则：
- 如果审查员要求修改，请重新实现
""",
    )


def create_code_reviewer():
    return AssistantAgent(
        name="CodeReviewer",
        model_client=model_client,
        system_message="""
你是代码审查专家。

规则：
- 代码有 bug → 说："请工程师修改"
- 问题来自需求 → 说："请产品经理重新评估"
- 代码合格 → 说："请测试工程师执行自动化测试"
""",
    )


def create_qa_engineer():
    return AssistantAgent(
        name="QualityAssurance",
        model_client=model_client,
        system_message="""
你是自动化测试工程师。

职责：
1. 接收代码审查员通过的代码
2. 编写并执行自动化测试脚本（Python / pytest / unittest）
3. 对 Streamlit 应用，可使用：
   - subprocess 启动应用
   - requests 测试接口
   - playwright / selenium（如需要）
4. 检查：
   - 程序是否能正常启动
   - 是否触发异常或崩溃
   - 是否符合需求描述

判定规则：
- 测试全部通过 → 说："请用户代理确认体验"
- 测试失败 / 报错 → 说："请工程师修复"
- 测试无法执行（缺依赖、无法启动）→ 说："请工程师修复"
- 发现需求与实现不一致 → 说："请产品经理重新评估"

注意：
- 必须输出测试代码
- 必须说明测试结果（Pass / Fail）
- 不要直接修改业务代码
""",
    )


def create_user_proxy():
    return UserProxyAgent(
        name="UserProxy",
        description="""
你是用户代理。
当测试工程师说"请用户代理确认体验"时，回复 "TERMINATE" 表示验收通过。
""",
    )


async def run_team_with_monitor(task: str):
    print("\n启动带对话监控的 SelectorGroupChat")
    print("=" * 60)

    monitor = create_dialogue_monitor(model_client)

    team = SelectorGroupChat(
        participants=[
            create_product_manager(),
            create_engineer(),
            create_code_reviewer(),
            create_qa_engineer(),
            create_user_proxy(),
        ],
        model_client=model_client,
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=30,
    )

    chat_messages: list[BaseChatMessage] = []

    async for message in team.run_stream(task=task):
        if isinstance(message, BaseChatMessage):
            chat_messages.append(message)
            print(f"\n[{message.source}]: {message.content[:200]}...")
        else:
            print(f"[{type(message).__name__}]")

        monitor_response = await monitor.on_messages(
            messages=chat_messages, cancellation_token=None
        )

        if "DIALOGUE_ANOMALY" in monitor_response.chat_message.content:
            print("\n检测到对话异常，强制终止")
            break

    print("\n协作结束")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(
        run_team_with_monitor(
            """
开发一个比特币价格显示 Streamlit 应用：

功能：
- 显示当前 BTC 价格（USD）
- 显示 24h 涨跌幅
- 提供刷新按钮

技术要求：
- 使用 Streamlit
- 调用 CoinGecko API
- 代码健壮、可运行
"""
        )
    )
