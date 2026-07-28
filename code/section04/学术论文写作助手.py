from typing import List, Dict, Any, Optional
from llm_client import HelloAgentsLLM
from enum import Enum


# ============================================================
# 模块 1: 反思维度定义
# ============================================================


class ReviewDimension(str, Enum):
    """论文评审的四个核心反思维度。"""

    LOGIC = "段落逻辑性"  # 段落衔接、论证链条、整体结构
    METHOD = "方法创新性"  # 方法的新颖度、与现有工作的差异化
    LANGUAGE = "语言表达"  # 语法、用词、句式多样性、学术写作规范
    CITATION = "引用规范性"  # 引用格式、文献相关性、引用充分性


# 每个维度对应的评审提示词模板
DIMENSION_PROMPTS = {
    ReviewDimension.LOGIC: """
你是一位顶会论文审稿人，专注于论文的**段落逻辑性**评审。
请严格评审以下论文草稿的：

1. **段落衔接**：段落之间是否有清晰的过渡句和逻辑连接？
2. **论证链条**：从问题提出到解决方案再到实验验证，逻辑是否环环相扣？
3. **结构完整性**：是否具备引言→相关工作→方法→实验→结论的标准结构？
4. **论点一致性**：全文的核心论点是否一致，没有前后矛盾？

论文草稿:
{content}

请逐条列出逻辑性问题，并为每条给出具体的修改建议。
如果该维度已无需改进，请在最后一行单独输出: [DIMENSION_OK]
""",
    ReviewDimension.METHOD: """
你是一位顶会论文审稿人，专注于论文的**方法创新性**评审。
请严格评审以下论文草稿的：

1. **新颖程度**：提出的方法与现有工作的核心差异是什么？是否只是简单组合？
2. **技术贡献**：方法的哪些部分是原创的？增量改进还是颠覆性创新？
3. **合理性**：方法设计是否有充分的动机和理论依据？
4. **可复现性**：方法描述是否足够详细，能够让其他研究者复现？

论文草稿:
{content}

请逐条列出创新性问题，并为每条给出具体的修改建议。
如果该维度已无需改进，请在最后一行单独输出: [DIMENSION_OK]
""",
    ReviewDimension.LANGUAGE: """
你是一位顶会论文的**语言润色**专家，母语为英语，精通学术写作规范。
请严格评审以下论文草稿的：

1. **语法与拼写**：是否存在语法错误、拼写错误或标点问题？
2. **用词准确性**：术语使用是否准确？是否有更优的学术表达方式？
3. **句式多样性**：是否过度使用某种句式（如过长复合句）？
4. **学术风格**：是否符合严谨、客观、简洁的学术写作风格？

论文草稿:
{content}

请逐条列出语言问题，并为每条给出具体的修改建议。
如果该维度已无需改进，请在最后一行单独输出: [DIMENSION_OK]
""",
    ReviewDimension.CITATION: """
你是一位顶会论文的**引用规范**评审专家，精通各大出版社的引用标准。
请严格评审以下论文草稿的：

1. **引用格式**：引用的格式是否统一且符合目标会议/期刊的标准？
2. **引用相关性**：每篇引用的文献是否与上下文紧密相关？
3. **引用完整性**：关键主张是否有充分的文献支撑？是否存在"孤儿断言"（无引用的重要声明）？
4. **参考文献列表**：参考文献信息是否完整（作者、标题、年份、出处）？

论文草稿:
{content}

请逐条列出引用问题，并为每条给出具体的修改建议。
如果该维度已无需改进，请在最后一行单独输出: [DIMENSION_OK]
""",
}


# ============================================================
# 模块 2: 记忆模块
# ============================================================


class AcademicMemory:
    """
    学术论文写作助手的记忆模块。
    不仅记录"版本"和"反馈"，还按维度分别存储评审记录，
    支持按维度查询历史反馈，用于退化检测和收敛判断。
    """

    def __init__(self):
        # 完整论文草稿版本历史 [v1, v2, v3, ...]
        self.drafts: List[str] = []

        # 按维度存储的历史反馈: {维度: [反馈1, 反馈2, ...]}
        self.review_history: Dict[ReviewDimension, List[str]] = {
            dim: [] for dim in ReviewDimension
        }

        # 是否被标记为 DIMENSION_OK (如果某维度已达标，后续轮次不再评审)
        self.dimension_done: Dict[ReviewDimension, bool] = {
            dim: False for dim in ReviewDimension
        }

    def add_draft(self, draft: str):
        """添加一版新的论文草稿。"""
        self.drafts.append(draft)

    def get_latest_draft(self) -> Optional[str]:
        """获取最新版本的论文草稿。"""
        return self.drafts[-1] if self.drafts else None

    def add_review(self, dimension: ReviewDimension, feedback: str):
        """添加某维度的评审反馈。"""
        self.review_history[dimension].append(feedback)

    def get_all_reviews(self, dimension: ReviewDimension) -> List[str]:
        """获取某维度的所有历史评审记录。"""
        return self.review_history[dimension]

    def mark_dimension_done(self, dimension: ReviewDimension):
        """标记某维度已达标，后续轮次跳过它的评审。"""
        self.dimension_done[dimension] = True

    def is_dimension_done(self, dimension: ReviewDimension) -> bool:
        """检查某维度是否已达标。"""
        return self.dimension_done[dimension]

    def active_dimensions(self) -> List[ReviewDimension]:
        """获取当前仍需评审的维度列表。"""
        return [dim for dim in ReviewDimension if not self.dimension_done[dim]]

    def all_dimensions_done(self) -> bool:
        """检查是否所有维度均已达标。"""
        return all(self.dimension_done.values())

    def is_review_degraded(self, dimension: ReviewDimension) -> bool:
        """
        退化检测：检查某维度的最近两次反馈是否相同。
        如果反馈开始重复，说明该维度评审已失去新意。
        """
        reviews = self.review_history[dimension]
        if len(reviews) < 2:
            return False
        return reviews[-1] == reviews[-2]

    def is_draft_converged(self) -> bool:
        """
        收敛检测：检查最近两版草稿是否完全相同。
        如果草稿不再变化，说明迭代已收敛。
        """
        if len(self.drafts) < 2:
            return False
        return self.drafts[-1] == self.drafts[-2]


# ============================================================
# 模块 3: Prompt 模板
# ============================================================

# 初稿生成提示词
DRAFT_PROMPT_TEMPLATE = """
你是一位资深学术论文作者，正在撰写一篇高质量的学术论文。
请根据以下选题信息和写作要求，生成论文的完整初稿。

# 选题信息
{topic}

# 写作要求
{instructions}

请生成包含以下完整章节的论文初稿：
1. 标题与摘要
2. 引言
3. 相关工作
4. 方法
5. 实验与分析
6. 结论

使用规范的学术语言，每个章节确保内容充实。
直接输出完整论文，不要包含额外的解释。
"""

# 多维度反思整合提示词（用于优化阶段）
REFINE_PROMPT_TEMPLATE = """
你是一位资深学术论文作者。你正在根据多位审稿人的反馈来优化你的论文。
请综合所有维度的反馈，输出一个改进后的完整新版本。

# 选题信息
{topic}

# 当前论文草稿
{current_draft}

# 本轮审稿反馈
{all_feedback}

请仔细阅读每条反馈，逐条响应，生成一个综合所有改进意见的新版本论文。
保持论文结构完整（标题与摘要、引言、相关工作、方法、实验与分析、结论）。
直接输出优化后的论文，不要包含额外的解释。
"""

# 终止条件判断提示词
TERMINATION_CHECK_PROMPT = """
判断以下评审反馈是否认为论文在某维度上仍需改进。

反馈:
{feedback}

如果反馈的核心结论是可以接受的、不阻碍发表的轻微问题 → 回答: FINISH
如果反馈要求实质性修改或指出严重缺陷 → 回答: CONTINUE
"""


# ============================================================
# 模块 4: 学术写作助手智能体
# ============================================================


class AcademicWritingAssistant:
    """
    学术论文写作助手：多维度 Reflection 智能体。

    核心流程：
      1. 生成初稿
      2. 每轮对每个活跃维度进行独立评审
      3. 标记已达标维度（DIMENSION_OK），后续跳过
      4. 所有维度达标时终止

    特点：
      - 四个独立反思维度：逻辑、方法、语言、引用
      - 按维度逐条生成反馈，避免"大杂烩"式评审
      - 维度级终止：每个维度独立判断是否达标
      - 收敛检测 + 退化检测 + 语义判定三重终止保障
    """

    def __init__(self, llm_client, max_rounds=5):
        self.llm_client = llm_client
        self.memory = AcademicMemory()
        self.max_rounds = max_rounds

    def run(self, topic: str, instructions: str = ""):
        """
        执行多维度反思-优化循环。

        参数:
        - topic: 论文选题（标题、核心问题、方法概述）
        - instructions: 额外的写作要求（格式、篇幅、目标会议等）
        """
        print(f"\n{'='*60}")
        print(f"📄 学术论文写作助手启动")
        print(f"选题: {topic}")
        print(f"{'='*60}")

        # === 第 1 步：生成初稿 ===
        print("\n--- 📝 步骤 1: 生成论文初稿 ---")
        prompt = DRAFT_PROMPT_TEMPLATE.format(topic=topic, instructions=instructions)
        initial_draft = self._get_llm_response(prompt)
        self.memory.add_draft(initial_draft)
        print("\n✅ 初稿生成完成。")

        # === 第 2 步：多轮多维反思与优化 ===
        for round_idx in range(self.max_rounds):
            print(f"\n{'='*60}")
            print(f"📋 第 {round_idx + 1}/{self.max_rounds} 轮迭代")
            print(f"{'='*60}")

            # 获取当前活跃维度（尚未达标的维度）
            active_dims = self.memory.active_dimensions()
            if not active_dims:
                print("\n✅ 所有维度均已达标，任务完成。")
                break

            print(f"\n本轮需评审维度: {[d.value for d in active_dims]}")

            # --- 第 2a 步：逐维度反思 ---
            current_draft = self.memory.get_latest_draft()
            round_feedback = {}  # {维度: 反馈文本}

            for dim in active_dims:
                print(f"\n--- 🔍 正在评审 [{dim.value}] ---")
                feedback = self._reflect(dim, current_draft)
                self.memory.add_review(dim, feedback)
                round_feedback[dim] = feedback

                # 检查该维度是否达标
                if feedback.strip().endswith("[DIMENSION_OK]"):
                    print(f"✅ 维度 [{dim.value}] 已达标，后续轮次跳过。")
                    self.memory.mark_dimension_done(dim)
                else:
                    # 退化检测：同一维度的反馈是否在重复
                    if self.memory.is_review_degraded(dim):
                        print(f"⚠️ 维度 [{dim.value}] 反馈趋于重复，强制达标。")
                        self.memory.mark_dimension_done(dim)

            # 再次检查是否所有维度已达标
            if self.memory.all_dimensions_done():
                print("\n✅ 所有维度均已达标，任务完成。")
                break

            # --- 第 2b 步：综合优化 ---
            print("\n--- ✏️ 正在根据多维反馈优化论文 ---")
            all_feedback_text = ""
            for dim, fb in round_feedback.items():
                all_feedback_text += f"[{dim.value} 评审意见]\n{fb}\n\n"

            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                topic=topic, current_draft=current_draft, all_feedback=all_feedback_text
            )
            refined_draft = self._get_llm_response(refine_prompt)
            self.memory.add_draft(refined_draft)

            # 收敛检测：新版本与旧版本完全相同
            if self.memory.is_draft_converged():
                print("\n✅ 草稿不再变化，判定已收敛，任务完成。")
                break

        # === 输出最终论文 ===
        final_draft = self.memory.get_latest_draft()
        print(f"\n{'='*60}")
        print("📄 最终论文")
        print(f"{'='*60}\n")
        print(final_draft)

        # === 打印报告摘要 ===
        self._print_summary_report()

        return final_draft

    def _reflect(self, dimension: ReviewDimension, draft: str) -> str:
        """
        在指定维度下对当前草稿进行反思评审。
        使用专门为该维度设计的评审提示词。
        """
        prompt_template = DIMENSION_PROMPTS[dimension]
        prompt = prompt_template.format(content=draft)
        feedback = self._get_llm_response(prompt)
        return feedback

    def _get_llm_response(self, prompt: str) -> str:
        """调用 LLM 获取响应。"""
        messages = [{"role": "user", "content": prompt}]
        response_text = self.llm_client.think(messages=messages) or ""
        return response_text

    def _print_summary_report(self):
        """打印整个过程的统计报告。"""
        print(f"\n{'='*60}")
        print("📊 写作过程统计报告")
        print(f"{'='*60}")
        print(f"总迭代轮次: {len(self.memory.drafts) - 1}")
        print(f"草稿版本数: {len(self.memory.drafts)}")
        print(f"\n各维度状态:")
        for dim in ReviewDimension:
            status = "✅ 已达标" if self.memory.is_dimension_done(dim) else "⏳ 未达标"
            review_count = len(self.memory.get_all_reviews(dim))
            print(f"  {dim.value}: {status} (评审 {review_count} 次)")


# ============================================================
# 主程序入口
# ============================================================

if __name__ == "__main__":
    try:
        llm_client = HelloAgentsLLM()
    except Exception as e:
        print(f"初始化LLM客户端时出错: {e}")
        exit()

    # 创建学术写作助手
    assistant = AcademicWritingAssistant(llm_client, max_rounds=3)

    # 示例：一篇关于强化学习的论文
    topic = """
标题: Efficient Exploration in Deep Reinforcement Learning via Intrinsic Curiosity
核心问题: 深度强化学习中，稀疏奖励环境下的智能体探索效率低下。
方法概述: 提出一种基于内在好奇心驱动的探索机制，通过预测下一状态的表征误差作为内在奖励信号，激励智能体探索未知状态空间。
目标: 在 Montezuma's Revenge 等稀疏奖励游戏中达到 SOTA 性能。
"""

    instructions = """
- 目标会议: NeurIPS 2026
- 篇幅: 8页正文 + 参考文献
- 格式: 遵循 NeurIPS 模板
- 引用: 不少于 30 篇参考文献
"""

    assistant.run(topic, instructions)
