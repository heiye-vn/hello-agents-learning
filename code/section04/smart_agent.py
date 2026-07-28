import json
import re
from typing import Optional, Tuple, Any, List
from datetime import datetime
from llm_client import HelloAgentsLLM
from tools import ToolExecutor

# ==================== 标准 ReAct 提示词模板 ====================
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。
当前系统时间：{current_date}


处理【最新/近期/时事】相关问题时的规则：
1. 必须基于当前系统时间进行检索，并在搜索关键词中包含具体年份（如：华为 2026年 最新手机）。
2. 在确认“最新”前，必须核实并比对产品的具体【发布时间/上市日期】。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""

# ==================== 纠错模式提示词模板 ====================
CORRECTIVE_PROMPT_TEMPLATE = """
你是一位经验丰富的智能体调试专家。智能体在调用工具时反复出错，需要你分析错误模式并给出纠错指导。

## 智能体的原始任务
Question: {question}

## 历史轨迹（含错误记录）
{history}

## 工具错误摘要
{error_summary}

请分析以下内容：
1. 错误的根本原因是什么？（工具名拼写错误？参数格式错误？工具选择策略错误？）
2. 给出具体的纠正建议，指导智能体下一步应该怎么做。
3. 如果需要，给出工具调用的正确示例。

请直接输出你的分析结果。
"""


class ToolErrorRecord:
    """记录工具调用过程中的错误，支持错误计数、摘要生成和同工具连续错误检测。"""

    def __init__(self, max_history: int = 5):
        self.errors: List[dict] = []  # 存储错误记录的列表
        self.max_history = max_history  # 最多保留的错误记录数

    def add_error(self, tool_name: str, tool_input: Any, error_msg: str, step: int):
        """添加一条新的工具调用错误记录。"""
        self.errors.append(
            {
                "step": step,
                "tool_name": tool_name,
                "tool_input": tool_input,
                "error": error_msg,
            }
        )
        if len(self.errors) > self.max_history:
            self.errors.pop(0)

    def get_error_summary(self) -> str:
        """生成人类可读的错误摘要文本，用于注入到纠错Prompt中。"""
        if not self.errors:
            return "暂无错误记录。"
        lines = []
        for e in self.errors:
            lines.append(
                f"  - 步骤{e['step']}: 调用工具 '{e['tool_name']}' 失败，错误: {e['error']}"
            )
        return "\n".join(lines)

    def consecutive_same_tool_errors(self, tool_name: str, threshold: int = 2) -> bool:
        """检测最近连续调用同一个工具是否失败超过阈值次数。"""
        count = 0
        for e in reversed(self.errors):
            if e["tool_name"] == tool_name:
                count += 1
            else:
                break
        return count >= threshold

    def total_errors(self) -> int:
        """返回当前的累计错误总数。"""
        return len(self.errors)

    def clear(self):
        """清空所有错误记录。"""
        self.errors.clear()


class StructuredParser:
    """解析LLM输出的结构化解析器，支持JSON格式和键值对格式，并提供模糊匹配工具名能力。"""

    def parse_output(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析LLM输出，提取Thought和Action。
        支持两种格式：
        1. JSON: {"thought": "...", "action": "..."}
        2. 键值对: Thought: ...\nAction: ...
        """
        # 优先尝试JSON格式解析
        try:
            data = json.loads(text.strip())
            thought = data.get("thought")
            action = data.get("action")
            if thought is not None and action is not None:
                return str(thought), str(action)
        except json.JSONDecodeError:
            pass

        # 回退到按行解析键值对格式
        lines = text.strip().split("\n")
        thought = None
        action = None

        for line in lines:
            if line.lower().startswith("thought:"):
                thought = line[8:].strip()
            elif line.lower().startswith("action:"):
                action = line[7:].strip()

        return thought, action

    def parse_action(self, action_text: str) -> Tuple[Optional[str], Optional[Any]]:
        """
        解析Action文本，提取工具名和输入参数。
        支持格式: ToolName[input]、JSON、空格分隔。
        """
        if not action_text:
            return None, None

        # 尝试JSON格式: {"name": "Search", "input": "..."}
        if action_text.startswith("{"):
            try:
                action_obj = json.loads(action_text)
                if isinstance(action_obj, dict):
                    action_name = action_obj.get("name")
                    action_input = action_obj.get("input", {})
                    return action_name, action_input
            except:
                pass

        # 标准格式: ToolName[input]
        if "[" in action_text and "]" in action_text:
            parts = action_text.split("[", 1)
            action_name = parts[0].strip()
            action_input = parts[1].rstrip("]")
            return action_name, self._safe_parse_input(action_input)

        # 简单空格分隔格式
        parts = action_text.split(maxsplit=1)
        if len(parts) == 2:
            return parts[0], parts[1]

        return action_text, None

    def _safe_parse_input(self, input_str: str) -> Any:
        """安全地解析输入字符串，优先尝试JSON解析，失败则返回原始字符串。"""
        try:
            return json.loads(input_str)
        except:
            return input_str

    def parse_action_with_fuzzy(
        self, action_text: str, available_tools: List[str]
    ) -> Tuple[Optional[str], Optional[Any], str]:
        """
        增强版Action解析：先调用parse_action，再对工具名做模糊匹配。
        返回 (工具名, 输入, 错误/建议信息)，空字符串表示正常。
        """
        tool_name, tool_input = self.parse_action(action_text)
        if tool_name is None:
            return None, None, "无法解析Action字段，请确保格式为 ToolName[input]"

        # 如果工具名不在可用列表中，尝试模糊匹配推荐
        if tool_name not in available_tools:
            suggestion = self._fuzzy_match_tool(tool_name, available_tools)
            return tool_name, tool_input, f"工具 '{tool_name}' 不存在。{suggestion}"

        return tool_name, tool_input, ""

    def _fuzzy_match_tool(self, wrong_name: str, available_tools: List[str]) -> str:
        """
        基于编辑距离（Levenshtein距离）的模糊匹配。
        当工具名拼写错误时，找出最相似的可用工具并给出推荐。
        """
        best_match = None
        best_score = 0

        for tool in available_tools:
            score = self._levenshtein_similarity(wrong_name.lower(), tool.lower())
            if score > best_score:
                best_score = score
                best_match = tool

        if best_match and best_score > 0.4:
            return f"您是否想使用 '{best_match}'？"
        return f"可用工具: {', '.join(available_tools)}"

    def _levenshtein_similarity(self, s1: str, s2: str) -> float:
        """计算两个字符串的编辑距离相似度，返回 0~1 之间的浮点数。"""
        if len(s1) == 0 and len(s2) == 0:
            return 1.0
        if len(s1) == 0 or len(s2) == 0:
            return 0.0

        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost
                )

        return 1 - dp[m][n] / max(m, n)


class SmartReActAgent:
    """
    带自动纠错机制的ReAct智能体。
    在标准ReAct循环（思考→行动→观察）基础上，增加了：
    - 工具调用错误记录与计数
    - 模糊匹配推荐正确工具名
    - 错误累计超阈值后自动切换为纠错Prompt模式
    """

    def __init__(
        self,
        llm_client: HelloAgentsLLM,
        tool_executor: ToolExecutor,
        max_steps: int = 8,
        error_threshold: int = 3,
    ):
        self.llm_client = llm_client  # LLM客户端，用于生成思考与行动
        self.tool_executor = tool_executor  # 工具执行器，管理和调用注册的工具
        self.max_steps = max_steps  # 最大运行步数
        self.error_threshold = error_threshold  # 触发纠错模式的错误次数阈值
        self.history = []  # 历史轨迹，记录每次Action和Observation
        self.parser = StructuredParser()  # 结构化输出解析器
        self.error_recorder = ToolErrorRecord()  # 工具调用错误记录器
        self.corrective_mode = False  # 是否已进入纠错模式

    def run(self, question: str):
        """主运行循环：ReAct循环 + 纠错模式切换。"""
        self.history = []
        self.error_recorder.clear()
        self.corrective_mode = False

        for step in range(1, self.max_steps + 1):
            print(f"\n{'='*50}")
            print(f"--- 第 {step} 步 ---")

            # 准备Prompt上下文
            tools_desc = self.tool_executor.getAvailableTools()
            available_tools = list(self.tool_executor.tools.keys())
            history_str = "\n".join(self.history)

            # 根据是否进入纠错模式，选择不同的Prompt模板
            if self.corrective_mode:
                prompt = self._build_corrective_prompt(
                    question, history_str, tools_desc
                )
            else:
                current_date = datetime.now().strftime("%Y年%m月%d日")
                prompt = REACT_PROMPT_TEMPLATE.format(
                    current_date=current_date,
                    tools=tools_desc,
                    question=question,
                    history=history_str,
                )

            # 调用LLM获取思考与行动
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            if not response_text:
                print("错误：LLM未能返回有效响应。")
                break

            # 解析LLM输出：提取Thought和Action
            thought, action = self.parser.parse_output(response_text)

            if thought:
                print(f"🤔 思考: {thought}")
            if not action:
                print("警告：未能解析出有效的Action，流程终止。")
                break

            # 如果LLM决定结束，提取最终答案
            if action.startswith("Finish"):
                # 优先使用 re.search + 贪婪匹配 (.*)，配合 re.DOTALL 兼容跨行文本
                match = re.search(r"Finish\[(.*)\]", action, re.DOTALL)
                if match:
                    final_answer = match.group(1).strip()
                    print(f"🎉 最终答案: {final_answer}")
                    return final_answer
                else:
                    # 容错兜底：若 LLM 忘记写末尾的 ']'，使用切片强行提取
                    print(
                        f"⚠️ 警告：Finish 正则未匹配成功，触发兜底提取。原始内容: {action}"
                    )
                    final_answer = action[7:].rstrip("]").strip()
                    print(f"🎉 最终答案(兜底): {final_answer}")
                    return final_answer

            # 解析Action并做模糊匹配检查
            tool_name, tool_input, fuzzy_msg = self.parser.parse_action_with_fuzzy(
                action, available_tools
            )

            # 处理Action完全无法解析的情况
            if tool_name is None:
                print(f"❌ {fuzzy_msg}")
                self.history.append(f"Action: {action}")
                self.history.append(f"Observation: {fuzzy_msg}")
                self.error_recorder.add_error("N/A", action, fuzzy_msg, step)
                continue

            # 处理工具名不匹配（模糊匹配给出了推荐信息）
            if fuzzy_msg:
                print(f"⚠️  警告: {fuzzy_msg}")
                self.history.append(f"Action: {action}")
                self.history.append(f"Observation: {fuzzy_msg}")
                self.error_recorder.add_error(tool_name, tool_input, fuzzy_msg, step)
                self._check_corrective_mode()
                continue

            # 执行工具调用
            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)

            if not tool_function:
                obs = f"错误：未找到名为 '{tool_name}' 的工具。"
                print(f"❌ {obs}")
                self.error_recorder.add_error(tool_name, tool_input, obs, step)
            else:
                try:
                    # 根据输入类型选择参数传递方式：字典解包 或 直接传字符串
                    if isinstance(tool_input, dict):
                        observation = tool_function(**tool_input)
                    else:
                        observation = tool_function(tool_input)
                    print(f"👀 观察: {observation}")
                    obs = str(observation)
                except Exception as e:
                    obs = f"工具执行异常: {type(e).__name__}: {e}"
                    print(f"❌ {obs}")
                    self.error_recorder.add_error(tool_name, tool_input, obs, step)

            # 记录Action和Observation到历史轨迹
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {obs}")

            # 每轮结束后检查是否需要进入纠错模式
            self._check_corrective_mode()

        print("已达到最大步数，流程终止。")
        return None

    def _build_corrective_prompt(
        self, question: str, history: str, tools_desc: str
    ) -> str:
        """
        构建纠错模式下的Prompt。
        在标准Prompt基础上，注入错误摘要和通用纠错指南，引导LLM反思错误模式。
        """
        error_summary = self.error_recorder.get_error_summary()
        total_errors = self.error_recorder.total_errors()

        header = (
            f"⚠️  系统检测到工具调用出现了 {total_errors} 次错误，智能体已自动进入纠错模式。\n"
            f"请仔细阅读以下错误摘要，分析原因并修正你的工具调用方式。\n"
        )

        return f"""
{header}

## 可用工具
{tools_desc}

## 工具错误记录
{error_summary}

## 通用纠错指南
1. 工具名必须拼写正确，区分大小写。
2. 工具输入格式必须正确（字符串或JSON对象）。
3. 如果工具调用连续失败，建议切换到其他相关工具或重新审视问题本身。
4. 不要重复调用同一个失败的工具而不改变输入。

## 历史轨迹
{history}

## 原始问题
Question: {question}

## 请根据以上信息，重新思考并输出正确的 Thought 和 Action。
"""

    def _check_corrective_mode(self):
        """检查累计错误是否达到阈值，如果是则切换为纠错模式。"""
        total = self.error_recorder.total_errors()
        if total >= self.error_threshold and not self.corrective_mode:
            print(f"\n🚨 工具调用已连续失败 {total} 次，进入纠错模式！")
            self.corrective_mode = True


if __name__ == "__main__":
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    calc_desc = (
        "一个数学计算器。能够计算复杂的数学表达式，支持加减乘除、括号、幂运算等。"
    )
    tool_executor.registerTool("Search", search_desc, __import__("tools").search)
    tool_executor.registerTool("Calculator", calc_desc, __import__("tools").calculator)

    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    agent = SmartReActAgent(llm, tool_executor, error_threshold=3)
    agent.run(question)
