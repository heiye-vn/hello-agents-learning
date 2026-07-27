import os
import sys
import ast
from pathlib import Path
from dotenv import load_dotenv
from serpapi import SerpApiClient
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta

# 兼容 Windows 终端控制台输出编码
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


load_dotenv(Path(__file__).parent / ".env")

"""
定义工具的三个核心要素：
1. 名称【name】:  一个简洁、唯一的标识符，供智能体在 Action 中调用，例如 Search。
2. 描述【Description】:  一段清晰的自然语言描述，说明这个工具的用途。这是整个机制中最关键的部分，因为大语言模型会依赖这段描述来判断何时使用哪个工具
3. 执行逻辑【Execution Logic】: 真正执行任务的函数或方法。
"""


def search(query: str) -> str:
    """
    一个基于 SerpApi / Tavily 的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔎 正在执行 [SerpApi] 网页搜索：{query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误: SERPAPI_API_KEY 未在 .env 中配置"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn",  # 语言代码
        }

        client = SerpApiClient(params)
        results = client.get_dict()

        # 智能解析：优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 {query} 的信息。"

    except Exception as e:
        return f"搜索时发生错误：{e}"


def calculator(expression: str) -> str:
    """
    一个用于执行数学计算的计算器工具。
    处理复杂的算术运算表达式（例如 '(123 + 456) * 789 / 12'）。
    """
    print(f"🧮 正在执行 [Calculator] 数学计算：{expression}")
    try:
        # 1. 预处理表达式字符串，清理常见字符和特殊符号
        expr_str = str(expression).strip()
        replacements = {
            "×": "*",
            "÷": "/",
            "（": "(",
            "）": ")",
            "=": "",
            "?": "",
            "？": "",
        }
        for old, new in replacements.items():
            expr_str = expr_str.replace(old, new)
        expr_str = expr_str.strip()

        # 2. 基于 AST 的安全算术表达式节点解析
        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Constant):  # 数值常量
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError(f"不支持的常量类型: {type(node.value)}")
            elif isinstance(node, ast.UnaryOp):  # 正负号 (+x, -x)
                operand = _eval(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                elif isinstance(node.op, ast.UAdd):
                    return +operand
                raise ValueError(f"不支持的一元运算符: {type(node.op)}")
            elif isinstance(node, ast.BinOp):  # 加减乘除等二元运算
                left = _eval(node.left)
                right = _eval(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    return left / right
                elif isinstance(node.op, ast.FloorDiv):
                    return left // right
                elif isinstance(node.op, ast.Mod):
                    return left % right
                elif isinstance(node.op, ast.Pow):
                    return left**right
                raise ValueError(f"不支持的二元运算符: {type(node.op)}")
            else:
                raise ValueError(f"不支持的语法结构: {type(node)}")

        parsed = ast.parse(expr_str, mode="eval")
        result = _eval(parsed)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


def current_time(*args, **kwargs):
    """获取当前时间（北京时间）的工具"""
    print(f"⌚️ 正在获取当前时间...")
    now = datetime.now(timezone(timedelta(hours=8)))
    return now.strftime("%Y-%m-%d %H:%M:%S")


class ToolExecutor:
    """工具执行器，负责管理和执行工具"""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """向工具箱中注册一个新工具。"""
        if name in self.tools:
            print(f"⚠️：工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"✅：工具 '{name} 注册成功。'")

    def getTool(self, name: str) -> callable:
        """根据名称获取一个工具的执行函数。"""
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """获取所有可用工具的格式化描述字符串"""
        return "\n".join(
            [f"- {name}: {info['description']}" for name, info in self.tools.items()]
        )


# --- 工具初始化与使用示例 ---
if __name__ == "__main__":
    # now_time = current_time()
    # print(now_time)

    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册搜索工具与计算器工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)

    calculator_description = (
        "一个计算器工具。用于计算数学表达式，例如 '(123 + 456) * 789 / 12'。"
    )
    toolExecutor.registerTool("Calculator", calculator_description, calculator)

    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 4. 智能体的 Action 调用示例
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")

    print("\n--- 执行 Action: Calculator['(123 + 456) × 789/ 12 = ?'] ---")
    calc_expression = "(123 + 456) × 789/ 12 = ?"
    calc_function = toolExecutor.getTool("Calculator")
    if calc_function:
        observation = calc_function(calc_expression)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 'Calculator' 的工具。")
