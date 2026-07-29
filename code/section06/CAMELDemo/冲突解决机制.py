# 1. Python 标准库（按字母升序排列）
import os
import sys
from pathlib import Path

# 2. 第三方依赖库（按字母升序排列，与标准库之间保留空行）
from camel.models import ModelFactory
from camel.societies import RolePlaying
from camel.types import ModelPlatformType
from camel.utils import print_text_animated
from colorama import Fore
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).parent / ".env")

# 冲突解决配置
CONFLICT_RESOLUTION_INTERVAL = 3  # 每 N 轮检测一次
QUALITY_THRESHOLD = 0.7  # 质量阈值（0~1），达到则强制结束
MIN_CONTENT_LENGTH = 200  # 最少有效字数才参与评分


def light_weight_scorer(content: str) -> float:
    """轻量级评分函数：综合考虑篇幅、结构完整性和主题覆盖度"""
    if not content or len(content) < MIN_CONTENT_LENGTH:
        return 0.0

    score = 0.0
    text = content.lower()

    # 1. 篇幅评分（0~0.4）：字数越多越好，目标 3000 字封顶
    word_count = len(content.replace(" ", "").replace("\n", ""))
    length_score = min(word_count / 3000, 1.0) * 0.4
    score += length_score

    # 2. 结构完整性（0~0.3）：检测章节标题关键词
    structure_keywords = [
        "引言",
        "第一章",
        "第二章",
        "第三章",
        "第四章",
        "第五章",
        "核心章节",
        "总结",
        "结语",
        "参考文献",
    ]
    structure_hits = sum(1 for kw in structure_keywords if kw in text)
    structure_score = min(structure_hits / 4, 1.0) * 0.3
    score += structure_score

    # 3. 主题覆盖度（0~0.3）：检测核心主题词
    topic_keywords = [
        "拖延",
        "心理",
        "认知",
        "行为",
        "改善",
        "建议",
        "案例",
        "实证",
        "研究",
        "时间管理",
        "自我",
        "情绪",
    ]
    topic_hits = sum(1 for kw in topic_keywords if kw in text)
    topic_score = min(topic_hits / 6, 1.0) * 0.3
    score += topic_score

    return round(score, 2)


# 创建模型,在这里以Qwen为例,调用的百炼大模型平台API
model = ModelFactory.create(
    model_platform=ModelPlatformType.QWEN,
    model_type=os.getenv("LLM_MODEL_ID"),
    url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

# 定义协作任务
task_prompt = """
创作一本关于"拖延症心理学"的短篇电子书，目标读者是对心理学感兴趣的普通大众。
要求：
1. 内容科学严谨，基于实证研究
2. 语言通俗易懂，避免过多专业术语
3. 包含实用的改善建议和案例分析
4. 篇幅控制在8000-10000字
5. 结构清晰，包含引言、核心章节和总结
"""

print(Fore.YELLOW + f"协作任务:\n{task_prompt}\n")
print(
    Fore.CYAN
    + f"[冲突解决] 每 {CONFLICT_RESOLUTION_INTERVAL} 轮自动评分，阈值 ≥ {QUALITY_THRESHOLD} 时强制结束\n"
)

# 初始化角色扮演会话
role_play_session = RolePlaying(
    assistant_role_name="心理学家",
    user_role_name="作家",
    task_prompt=task_prompt,
    model=model,
)

print(Fore.CYAN + f"具体任务描述:\n{role_play_session.task_prompt}\n")

# 开始协作对话
chat_turn_limit, n = 30, 0
input_msg = role_play_session.init_chat()
full_content = ""

while n < chat_turn_limit:
    n += 1
    assistant_response, user_response = role_play_session.step(input_msg)

    user_content = user_response.msg.content
    assistant_content = assistant_response.msg.content

    print_text_animated(Fore.BLUE + f"作家:\n\n{user_content}\n")
    print_text_animated(Fore.GREEN + f"心理学家:\n\n{assistant_content}\n")

    # 累积对话生成的内容
    full_content += "\n" + user_content + "\n" + assistant_content

    # 冲突解决：每 N 轮检测一次
    if n % CONFLICT_RESOLUTION_INTERVAL == 0:
        quality_score = light_weight_scorer(full_content)
        print(
            Fore.MAGENTA
            + f"[冲突解决] 第 {n} 轮评分: {quality_score:.2f} / 阈值: {QUALITY_THRESHOLD}"
        )
        if quality_score >= QUALITY_THRESHOLD:
            print(
                Fore.RED
                + f"[冲突解决] 评分 {quality_score:.2f} 达到阈值 {QUALITY_THRESHOLD}，强行结束任务！"
            )
            break

    # 检查任务完成标志
    if "CAMEL_TASK_DONE" in user_response.msg.content:
        print(Fore.MAGENTA + "✅ 电子书创作完成！")
        break

    input_msg = assistant_response.msg

print(Fore.YELLOW + f"总共进行了 {n} 轮协作对话")
