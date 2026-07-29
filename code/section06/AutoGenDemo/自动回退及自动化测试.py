import os
import asyncio

from typing import List, Dict, Any
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

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


# -----------------------------
# 智能体（Agent）
# -----------------------------
def create_product_manager():
    """创建产品经理智能体：负责分析需求、输出技术方案与验收标准"""
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
    """创建工程师智能体：负责根据需求编写可运行的 Python 代码"""
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
    """创建代码审查员智能体：负责检查代码质量和需求一致性"""
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


def create_user_proxy():
    """创建用户代理智能体：负责模拟用户进行最终验收确认"""
    return UserProxyAgent(
        name="UserProxy",
        description="""
你是用户代理。
当测试工程师说"请用户代理确认体验"时，回复 "TERMINATE" 表示验收通过。
""",
    )


def create_qa_engineer():
    """创建 QA 测试工程师智能体：负责编写并执行自动化测试"""
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


# -----------------------------
# 团队协作
# -----------------------------
async def run_team(task: str):
    """启动多智能体软件开发团队，围绕给定任务进行协作"""
    print("\n🚀 启动 SelectorGroupChat 软件开发团队")
    print("=" * 60)

    team = SelectorGroupChat(
        participants=[
            create_product_manager(),
            create_engineer(),
            create_code_reviewer(),
            create_qa_engineer(),
            create_user_proxy(),
        ],
        model_client=model_client,
        termination_condition=TextMentionTermination(
            "TERMINATE"
        ),  # 当任一智能体说出 TERMINATE 时结束
        max_turns=25,  # 最大对话轮次，防止无限循环
    )

    # 流式运行团队协作，并在控制台实时输出对话过程
    await Console(team.run_stream(task=task))

    print("\n✅ 协作结束")
    print("=" * 60)


# -----------------------------
# 测试用例
# -----------------------------
async def demo_normal_requirement():
    """测试场景 1：正常需求 —— 开发比特币价格显示的 Streamlit 应用"""
    await run_team(
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


async def demo_changed_requirement():
    """测试场景 2：需求变更 —— 将 24h 涨跌幅改为 7 天走势图，触发跨智能体回退协商"""
    await run_team(
        """
开发一个比特币价格显示应用。

功能：
- 显示 BTC 当前价格
- 显示 7 天价格走势图（折线图）

注意：之前的需求只要求显示24h涨跌幅，现在需要改成7天走势图。
请团队协作完成修改。
"""
    )


# -----------------------------
# 主入口
# -----------------------------
if __name__ == "__main__":
    # 如需切换场景，取消注释对应的行即可
    asyncio.run(demo_normal_requirement())
    # asyncio.run(demo_changed_requirement())
