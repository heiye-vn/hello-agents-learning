"""
AutoGen v0.4 强类型结构化多智能体软件开发团队协作案例
使用 Pydantic 约束 Agent 结构化输出，消除文本匹配模式与格式不确定性。
"""

import os
import sys
from pathlib import Path
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 确保控制台编码为 UTF-8，防止 Windows 终端下字符编码报错
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 加载 .env 环境变量
load_dotenv(Path(__file__).parent / ".env")

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console


# ================= 1. 定义 Pydantic 强类型数据模型 =================


class RequirementAnalysis(BaseModel):
    """产品经理输出的需求分析模型"""

    title: str = Field(description="应用名称")
    core_features: List[str] = Field(description="核心功能列表")
    technical_stack: List[str] = Field(description="技术选型建议")
    acceptance_criteria: List[str] = Field(description="验收标准")


class CodeImplementation(BaseModel):
    """工程师输出的代码实现模型"""

    description: str = Field(description="实现方案与设计说明")
    code: str = Field(description="完整的可运行 Python 代码")
    dependencies: List[str] = Field(description="所需第三方依赖列表")


class CodeReviewReport(BaseModel):
    """代码审查员输出的审查报告与最终修复代码模型"""

    quality_score: int = Field(description="代码质量评分 (0-100)")
    is_approved: bool = Field(description="是否审核通过")
    review_comments: List[str] = Field(description="详细的审查意见与注意事项")
    final_code: str = Field(description="根据审查意见优化修补后的最终完整 Python 代码")


# ================= 2. 模型客户端初始化 =================

import json
import re


# ================= 2. 强类型解析与模型客户端初始化 =================


def parse_structured_response(response_text: str, schema_cls: type[BaseModel]):
    """
    通用强类型解析辅助函数：
    自动从 Agent 输出中提取 JSON 并校验反序列化为 Pydantic 对象，容忍 Markdown 代码块与杂讯文本。
    """
    text = response_text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx : end_idx + 1]

    return schema_cls.model_validate_json(text)


def create_model_client():
    """创建适配第三方 LLM API 的 OpenAI 客户端"""
    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID", "gpt-4o"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": "unknown",
        },
    )


# ================= 3. 运行 v0.4 强类型协作流水线 =================


async def run_v4_software_development_team():
    """运行 AutoGen v0.4 结构化 Agent 软件开发团队"""
    print("🚀 启动 AutoGen v0.4 结构化多智能体流水线...")
    print("=" * 60)

    model_client = create_model_client()

    # 1. 初始化产品经理智能体
    pm_schema_prompt = json.dumps(
        RequirementAnalysis.model_json_schema(), ensure_ascii=False
    )
    product_manager = AssistantAgent(
        name="ProductManager",
        model_client=model_client,
        system_message=(
            "你是一位资深产品经理，负责对用户需求进行结构化分析。\n"
            f"你必须仅输出符合以下 JSON Schema 的 JSON 对象：\n{pm_schema_prompt}"
        ),
    )

    # 2. 初始化软件工程师智能体
    eng_schema_prompt = json.dumps(
        CodeImplementation.model_json_schema(), ensure_ascii=False
    )
    engineer = AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message=(
            "你是一位资深软件工程师，负责根据产品分析编写高质量的 Streamlit Python 代码。\n"
            "代码中必须包含良好的异常处理与抗风险逻辑。\n"
            f"你必须仅输出符合以下 JSON Schema 的 JSON 对象：\n{eng_schema_prompt}"
        ),
    )

    # 3. 初始化代码审查员智能体
    review_schema_prompt = json.dumps(
        CodeReviewReport.model_json_schema(), ensure_ascii=False
    )
    code_reviewer = AssistantAgent(
        name="CodeReviewer",
        model_client=model_client,
        system_message=(
            "你是一位严格的代码审查专家。请仔细检查工程师的代码，检查安全陷阱、"
            "性能死角与 UI 暗黑模式对比度，并在 final_code 字段中输出经过完善修订后的完整 Python 代码。\n"
            f"你必须仅输出符合以下 JSON Schema 的 JSON 对象：\n{review_schema_prompt}"
        ),
    )

    # 开发任务定义
    user_task = """你需要开发一个比特币价格实时显示 Web 应用，要求：
1. 界面简洁美观，支持显示比特币当前价格 (USD)、24小时涨跌额与涨跌幅。
2. 包含刷新功能按钮。
3. 必须具备良好的错误处理与多数据源容错（规避单一 API 451 地区限流问题）。
4. 适配暗黑/深色模式下的高对比度卡片样式，避免白底白字看不清的问题。"""

    print(f"\n📋 [任务发起]：{user_task}\n")

    # 步骤一：产品经理生成需求文档
    print("👤 [1/3] ProductManager 正在分析需求...")
    pm_response = await product_manager.on_messages(
        [TextMessage(content=user_task, source="user")],
        cancellation_token=None,
    )
    pm_analysis: RequirementAnalysis = parse_structured_response(
        pm_response.chat_message.content, RequirementAnalysis
    )
    print(f"✅ 需求分析完成：标题为 《{pm_analysis.title}》")

    # 步骤二：工程师根据需求编写代码
    print("\n💻 [2/3] Engineer 正在根据分析结果进行代码构建...")
    engineer_input = f"""请根据以下需求设计构建应用：
标题：{pm_analysis.title}
核心功能：{', '.join(pm_analysis.core_features)}
技术栈建议：{', '.join(pm_analysis.technical_stack)}
验收标准：{', '.join(pm_analysis.acceptance_criteria)}
"""
    eng_response = await engineer.on_messages(
        [TextMessage(content=engineer_input, source="ProductManager")],
        cancellation_token=None,
    )
    eng_code: CodeImplementation = parse_structured_response(
        eng_response.chat_message.content, CodeImplementation
    )
    print(f"✅ 代码开发完成，已包含依赖包: {eng_code.dependencies}")

    # 步骤三：代码审查员进行评审与代码修补
    print("\n🔍 [3/3] CodeReviewer 正在评审代码与进行最终重构...")
    reviewer_input = f"""请审查以下代码并做出改进修补：
实现说明：{eng_code.description}

待审查代码：
```python
{eng_code.code}
```
"""
    review_response = await code_reviewer.on_messages(
        [TextMessage(content=reviewer_input, source="Engineer")],
        cancellation_token=None,
    )
    review_report: CodeReviewReport = parse_structured_response(
        review_response.chat_message.content, CodeReviewReport
    )

    print("\n" + "=" * 60)
    print("🎉 团队协作全流程完成！")
    print(f"📊 代码质量得分: {review_report.quality_score} / 100")
    print(f"✅ 审查结论: {'审核通过' if review_report.is_approved else '调整后通过'}")
    print("💬 审查意见:")
    for comment in review_report.review_comments:
        print(f"  - {comment}")

    # 直接从强类型 Pydantic 对象中获取 final_code，保存落地为 auto_generated_app.py
    output_path = Path(__file__).parent / "auto_generated_app.py"
    output_path.write_text(review_report.final_code, encoding="utf-8")

    print(f"\n💾 已直接通过 Pydantic 对象精准导出最终文件：\n   --> {output_path}")
    print(f"🚀 可以使用以下命令直接运行生成的应用：\n   streamlit run {output_path}")

    return review_report

    print("\n" + "=" * 60)
    print("🎉 团队协作全流程完成！")
    print(f"📊 代码质量得分: {review_report.quality_score} / 100")
    print(f"✅ 审查结论: {'审核通过' if review_report.is_approved else '调整后通过'}")
    print("💬 审查意见:")
    for comment in review_report.review_comments:
        print(f"  - {comment}")

    # 直接从 Pydantic 模型中点出 final_code，保存落地
    output_path = Path(__file__).parent / "auto_generated_app.py"
    output_path.write_text(review_report.final_code, encoding="utf-8")

    print(f"\n💾 已直接通过 Pydantic 对象准确导出最终文件：\n   --> {output_path}")
    print(f"🚀 可以使用以下命令直接运行生成的应用：\n   streamlit run {output_path}")

    return review_report


# 主程序入口
if __name__ == "__main__":
    try:
        asyncio.run(run_v4_software_development_team())
    except Exception as e:
        print(f"❌ 运行过程中发生错误: {e}")
        import traceback

        traceback.print_exc()
