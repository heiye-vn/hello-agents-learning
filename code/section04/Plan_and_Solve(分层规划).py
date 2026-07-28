"""智能体范式 —— Plan-and-Solve【先规划, 后执行】"""

import os
import ast
import json
from llm_client import HelloAgentsLLM
from dotenv import load_dotenv
from typing import List, Dict, Tuple

try:
    load_dotenv()
except FileNotFoundError:
    print("警告：未找到 .env 文件，将使用系统环境变量。")
except Exception as e:
    print(f"警告：加载 .env 文件时出错: {e}")


# ============================================================
# 提示词模板
# ============================================================

# 高层规划提示词：生成粗粒度的抽象步骤
HIGH_LEVEL_PLANNER_PROMPT = """
你是一位顶级的AI架构师。你的任务是为复杂问题制定一个**高层次**的抽象行动计划。
每个高层步骤应是一个**粗粒度的阶段/模块**，描述"做什么"而非"怎么做"。
步骤之间需保持逻辑顺序，数量控制在 2~5 个。

问题: {question}

请严格按照以下格式输出，```python与```作为前后缀是必要的:
```python
["高层步骤1: xxx", "高层步骤2: xxx", "高层步骤3: xxx"]
```
"""

# 子规划提示词：将一个高层步骤展开为详细子步骤
SUB_PLANNER_PROMPT = """
你是一位顶级的AI规划专家。你的任务是将一个**高层抽象步骤**展开为多个**具体的、可执行的详细子步骤**。

原始问题: {question}
完整的高层计划: {high_level_plan}
当前需要展开的高层步骤: {high_level_step}
已完成的子步骤与结果（来自之前的高层步骤）: {completed_sub_steps}

请为当前高层步骤生成详细的子步骤计划。
每个子步骤必须是一个可以独立执行的明确任务。
请严格按照以下格式输出，```python与```作为前后缀是必要的:
```python
["子步骤1: xxx", "子步骤2: xxx", "子步骤3: xxx", ...]
```
"""

# 子步骤执行提示词
SUB_EXECUTOR_PROMPT = """
你是一位顶级的AI执行专家。你正在执行一个**子步骤**，属于一个更大的高层步骤的一部分。

原始问题: {question}
高层计划: {high_level_plan}
当前高层步骤: {high_level_step}
当前子步骤: {current_sub_step}
历史子步骤与结果: {history}

请只输出当前子步骤的执行结果，不要额外解释。
"""

# 子步骤验证提示词
SUB_VERIFICATION_PROMPT = """
你是一位任务质量评审专家。请判断以下子步骤的执行结果是否成功。

原始问题: {question}
高层步骤: {high_level_step}
子步骤: {sub_step}
执行结果: {result}

成功标准：结果包含有效数据或明确答案。
失败标准：结果为空、包含错误信息、或明显不正确。
请只回答 "SUCCESS" 或 "FAILURE"。
"""

# 子步骤重规划提示词
SUB_REPLAN_PROMPT = """
你是一位顶级的AI规划专家。一个子步骤执行**失败**，需要重新规划**当前高层步骤内**的剩余子步骤。

原始问题: {question}
高层计划: {high_level_plan}
当前高层步骤: {high_level_step}
本高层步骤内已完成的子步骤与结果: {completed_in_high_level}
失败的子步骤: {failed_sub_step}
失败原因: {failure_reason}

请为当前高层步骤内**剩余未完成的部分**重新生成子步骤计划。
新计划必须跳过已完成的子步骤，修复或替换失败的子步骤。
请严格按照以下格式输出，```python与```作为前后缀是必要的:
```python
["新子步骤1", "新子步骤2", ...]
```
"""


# ============================================================
# 分层规划器
# ============================================================


class HierarchicalPlanner:
    """
    分层规划器：
    1. 先生成 2~5 个高层抽象步骤
    2. 执行到某个高层步骤时，再将该步骤展开为详细子步骤
    """

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def plan_high_level(self, question: str) -> list[str]:
        """生成高层抽象计划（粗粒度）"""
        prompt = HIGH_LEVEL_PLANNER_PROMPT.format(question=question)
        messages = [{"role": "user", "content": prompt}]

        print("\n--- 正在生成高层抽象计划 ---")
        response_text = self.llm_client.think(messages=messages) or ""
        print(f"✅ 高层计划已生成:\n{response_text}")

        return self._parse_plan(response_text)

    def plan_sub_steps(
        self,
        question: str,
        high_level_plan: list[str],
        high_level_step: str,
        completed_sub_steps: str,
    ) -> list[str]:
        """将一个高层步骤展开为详细的子步骤"""
        prompt = SUB_PLANNER_PROMPT.format(
            question=question,
            high_level_plan=high_level_plan,
            high_level_step=high_level_step,
            completed_sub_steps=completed_sub_steps if completed_sub_steps else "无",
        )
        messages = [{"role": "user", "content": prompt}]

        print(f"\n--- 正在展开高层步骤: [{high_level_step}] ---")
        response_text = self.llm_client.think(messages=messages) or ""
        print(f"✅ 子步骤计划已生成:\n{response_text}")

        return self._parse_plan(response_text)

    def replan_sub_steps(
        self,
        question: str,
        high_level_plan: list[str],
        high_level_step: str,
        completed_in_high_level: str,
        failed_sub_step: str,
        failure_reason: str,
    ) -> list[str]:
        """当某高层步骤内的子步骤失败时，重新规划该高层步骤的剩余子步骤"""
        prompt = SUB_REPLAN_PROMPT.format(
            question=question,
            high_level_plan=high_level_plan,
            high_level_step=high_level_step,
            completed_in_high_level=(
                completed_in_high_level if completed_in_high_level else "无"
            ),
            failed_sub_step=failed_sub_step,
            failure_reason=failure_reason,
        )
        messages = [{"role": "user", "content": prompt}]

        print(f"\n--- 正在重新规划高层步骤内的子步骤: [{high_level_step}] ---")
        response_text = self.llm_client.think(messages=messages) or ""
        print(f"✅ 新子步骤计划已生成:\n{response_text}")

        return self._parse_plan(response_text)

    def _parse_plan(self, response_text: str) -> list[str]:
        try:
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


# ============================================================
# 分层执行器
# ============================================================


class HierarchicalExecutor:
    """
    分层执行器：
    - 逐层遍历高层步骤
    - 进入每个高层步骤时，先展开为子步骤再逐个执行
    - 子步骤失败时触发当前高层步骤内的重规划
    """

    def __init__(
        self,
        llm_client: HelloAgentsLLM,
        planner: HierarchicalPlanner,
        max_replan_per_high_level: int = 3,
    ):
        self.llm_client = llm_client
        self.planner = planner
        self.max_replan_per_high_level = max_replan_per_high_level

    def _verify_sub_step(
        self, question: str, high_level_step: str, sub_step: str, result: str
    ) -> bool:
        prompt = SUB_VERIFICATION_PROMPT.format(
            question=question,
            high_level_step=high_level_step,
            sub_step=sub_step,
            result=result,
        )
        messages = [{"role": "user", "content": prompt}]
        response = self.llm_client.think(messages=messages) or ""
        return "SUCCESS" in response.upper()

    def _execute_high_level_step(
        self,
        question: str,
        high_level_plan: list[str],
        high_level_step: str,
        high_level_index: int,
        global_history: str,
    ) -> Tuple[str, str]:
        """
        执行单个高层步骤：
        1. 展开为子步骤
        2. 逐条执行子步骤（含验证和重规划）
        3. 返回该高层步骤的汇总结果 + 更新的全局历史
        """
        print(f"\n{'='*50}")
        print(f"进入高层步骤 {high_level_index}: {high_level_step}")
        print(f"{'='*50}")

        # 将该高层步骤展开为详细子步骤
        sub_plan = self.planner.plan_sub_steps(
            question, high_level_plan, high_level_step, global_history
        )
        if not sub_plan:
            return (
                f"[高层步骤 {high_level_index} 失败] 无法生成子步骤计划",
                global_history,
            )

        sub_history = ""  # 当前高层步骤内的子步骤历史
        sub_index = 0  # 当前子步骤索引
        replan_count = 0  # 当前高层步骤内的重规划次数
        high_level_result = ""  # 该高层步骤的最终汇总结果

        while sub_index < len(sub_plan):
            current_sub_plan = sub_plan[sub_index:]
            sub_step = sub_plan[sub_index]
            sub_step_number = sub_index + 1

            print(f"\n  -> 执行子步骤 {sub_step_number}/{len(sub_plan)}: {sub_step}")

            prompt = SUB_EXECUTOR_PROMPT.format(
                question=question,
                high_level_plan=high_level_plan,
                high_level_step=high_level_step,
                current_sub_step=sub_step,
                history=sub_history if sub_history else "无",
            )
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages) or ""

            record = (
                f"  子步骤 {sub_step_number}: {sub_step}\n  结果: {response_text}\n\n"
            )
            sub_history += record
            high_level_result = response_text
            print(f"  ✅ 子步骤 {sub_step_number} 执行完毕: {response_text}")

            # 验证子步骤结果
            is_success = self._verify_sub_step(
                question, high_level_step, sub_step, response_text
            )

            if is_success:
                print(f"    ✓ 子步骤 {sub_step_number} 验证通过")
                sub_index += 1
            else:
                print(f"    ✗ 子步骤 {sub_step_number} 验证失败")
                replan_count += 1
                if replan_count > self.max_replan_per_high_level:
                    print(f"    ⛔ 该高层步骤内重规划次数已达上限，终止")
                    return (
                        f"[高层步骤 {high_level_index} 失败] 子步骤重规划超限",
                        global_history,
                    )

                print(
                    f"    🔄 正在重新规划高层步骤 [{high_level_step}] 内的剩余子步骤..."
                )
                new_sub_plan = self.planner.replan_sub_steps(
                    question,
                    high_level_plan,
                    high_level_step,
                    sub_history,
                    sub_step,
                    response_text,
                )
                if not new_sub_plan:
                    print(f"    ❌ 子步骤重规划失败，终止该高层步骤")
                    return (
                        f"[高层步骤 {high_level_index} 失败] 重规划返回空",
                        global_history,
                    )

                sub_plan = sub_plan[:sub_index] + new_sub_plan
                print(f"    📋 更新后子步骤计划: {sub_plan}")

        # 该高层步骤全部完成，将子步骤结果汇总到全局历史
        summary = f"高层步骤 {high_level_index}: {high_level_step}\n执行详情:\n{sub_history}\n"
        global_history += summary
        print(f"\n✅ 高层步骤 {high_level_index} [{high_level_step}] 全部完成")
        return (high_level_result, global_history)

    def execute(self, question: str, high_level_plan: list[str]) -> str:
        """遍历所有高层步骤并依次执行"""
        global_history = ""
        final_answer = ""

        print("\n--- 开始分层执行 ---")
        for i, high_level_step in enumerate(high_level_plan, 1):
            result, global_history = self._execute_high_level_step(
                question, high_level_plan, high_level_step, i, global_history
            )
            final_answer = result

            # 检查高层步骤是否失败
            if result.startswith("[高层步骤"):
                print(f"\n❌ 高层步骤 {i} 执行失败，终止整个任务")
                return result

        return final_answer


# ============================================================
# 分层规划智能体
# ============================================================


class HierarchicalPlanningAgent:
    """分层规划智能体"""

    def __init__(self, llm_client: HelloAgentsLLM, max_replan_per_high_level: int = 3):
        self.llm_client = llm_client
        self.planner = HierarchicalPlanner(llm_client)
        self.executor = HierarchicalExecutor(
            llm_client, self.planner, max_replan_per_high_level
        )

    def run(self, question: str):
        print(f"\n--- 开始处理问题 ---\n问题: {question}")
        high_level_plan = self.planner.plan_high_level(question)
        if not high_level_plan:
            print("\n--- 任务终止 --- \n无法生成高层计划。")
            return
        print(f"\n📋 高层计划: {high_level_plan}")
        final_answer = self.executor.execute(question, high_level_plan)
        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")


if __name__ == "__main__":
    try:
        llm_client = HelloAgentsLLM()
        agent = HierarchicalPlanningAgent(llm_client, max_replan_per_high_level=2)
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        agent.run(question)
    except ValueError as e:
        print(e)
