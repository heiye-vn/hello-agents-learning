import re
import os
from dotenv import load_dotenv
from wttrin import *
from search_attraction import *
from OpenAICompatibleClient import *

from OpenAICompatibleClient import OpenAICompatibleClient

load_dotenv()

# 用户记忆模块
user_memory = {
    "preferences": [],  # 兴趣偏好，如 ["历史文化", "自然风光"]
    "budget_min": 0,
    "budget_max": float("inf"),
    "rejection_count": 0,  # 连续拒绝次数
    "rejected_ids": [],  # 被拒绝的景点ID/名称，避免重复推荐
    "interaction_count": 0,  # 总交互次数
    "last_strategy": "default",
}


# 记忆管理函数
def update_preferences(interest=None, budget_min=None, budget_max=None):
    if interest and interest.strip():
        if interest not in user_memory["preferences"]:
            user_memory["preferences"].append(interest)
    if budget_min and str(budget_min).strip():
        user_memory["budget_min"] = int(budget_min)
    if budget_max and str(budget_max).strip():
        user_memory["budget_max"] = int(budget_max)
    return f"偏好已更新。当前兴趣: {user_memory['preferences']}, 预算: {user_memory['budget_min']}-{user_memory['budget_max']}"


def get_ticket_status(attraction_id=None, attraction_name=None, city=None):
    # 模拟票务查询，实际可对接API
    return f"门票状态: 已售罄 (景点: {attraction_name or attraction_id or city})"


def query_attractions_by_category(category, exclude_id=None, city=None):
    # 模拟搜索同类景点的数据
    mock_db = {
        "历史文化": [
            {
                "id": "a1",
                "name": "故宫博物院",
                "rating": 4.9,
                "price": 60,
                "tags": ["历史文化"],
                "desc": "明清皇家宫殿",
            },
            {
                "id": "a2",
                "name": "天坛公园",
                "rating": 4.7,
                "price": 35,
                "tags": ["历史文化"],
                "desc": "明清帝王祭天场所",
            },
            {
                "id": "a3",
                "name": "颐和园",
                "rating": 4.8,
                "price": 50,
                "tags": ["历史文化"],
                "desc": "皇家园林",
            },
        ],
        "自然风光": [
            {
                "id": "b1",
                "name": "黄山",
                "rating": 4.9,
                "price": 190,
                "tags": ["自然风光"],
                "desc": "天下第一奇山",
            },
            {
                "id": "b2",
                "name": "九寨沟",
                "rating": 4.8,
                "price": 169,
                "tags": ["自然风光"],
                "desc": "童话世界",
            },
            {
                "id": "b3",
                "name": "西湖",
                "rating": 4.7,
                "price": 0,
                "tags": ["自然风光"],
                "desc": "人间天堂",
            },
        ],
        "主题乐园": [
            {
                "id": "c1",
                "name": "上海迪士尼",
                "rating": 4.8,
                "price": 499,
                "tags": ["主题乐园"],
                "desc": "奇幻童话王国",
            },
            {
                "id": "c2",
                "name": "北京环球影城",
                "rating": 4.7,
                "price": 418,
                "tags": ["主题乐园"],
                "desc": "电影主题乐园",
            },
        ],
        "general": [
            {
                "id": "d1",
                "name": "长城",
                "rating": 4.9,
                "price": 45,
                "tags": ["历史文化", "地标"],
                "desc": "世界文化遗产",
            },
            {
                "id": "d2",
                "name": "国家博物馆",
                "rating": 4.6,
                "price": 0,
                "tags": ["历史文化"],
                "desc": "中华文明瑰宝",
            },
        ],
    }
    results = mock_db.get(category, mock_db["general"])
    if exclude_id:
        results = [r for r in results if r["id"] != exclude_id]
    if city:
        results = [r for r in results if city in r.get("desc", "")]

    # 包装为简单对象以支持 .name / .rating / .price / .tags / .desc 属性
    class AttrObj:
        def __init__(self, d):
            self.id = d["id"]
            self.name = d["name"]
            self.rating = d["rating"]
            self.price = d["price"]
            self.tags = d["tags"]
            self.desc = d["desc"]

        def __repr__(self):
            return f"{self.name}({self.rating}分, ¥{self.price})"

    return [AttrObj(r) for r in results]


def get_alternative_attractions(category, original_id=None, reason="sold_out"):
    alternatives = query_attractions_by_category(category, exclude_id=original_id)
    # 按用户偏好过滤
    if user_memory["preferences"]:
        filtered = []
        for attr in alternatives:
            if any(pref in attr.tags for pref in user_memory["preferences"]):
                filtered.append(attr)
        if filtered:
            alternatives = filtered
    # 按预算过滤
    alternatives = [
        a
        for a in alternatives
        if user_memory["budget_min"] <= a.price <= user_memory["budget_max"]
    ]
    # 排除已拒绝的
    alternatives = [
        a
        for a in alternatives
        if a.id not in user_memory["rejected_ids"]
        and a.name not in user_memory["rejected_ids"]
    ]
    if reason == "sold_out":
        alternatives.sort(key=lambda x: x.rating, reverse=True)
    return alternatives[:3]


def refine_recommendation_strategy(rejection_pattern=None):
    # 根据用户拒绝模式切换策略
    prefs = user_memory["preferences"]
    if "自然风光" in prefs:
        strategy = "自然风光优先"
    elif "历史文化" in prefs:
        strategy = "历史文化优先"
    elif rejection_pattern and len(rejection_pattern) > 0:
        strategy = f"尝试推荐与 {rejection_pattern[-1]} 相关的景点"
    else:
        strategy = "换一个不同类型推荐"
    user_memory["last_strategy"] = strategy
    return f"推荐策略已调整为: {strategy}。后续推荐将优先考虑{strategy}。"


def reset_rejection_count():
    user_memory["rejection_count"] = 0
    return "拒绝计数已重置。"


# 将所有工具函数放入字典
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
    "get_ticket_status": get_ticket_status,
    "update_preferences": update_preferences,
    "get_alternative_attractions": get_alternative_attractions,
    "refine_recommendation_strategy": refine_recommendation_strategy,
    "reset_rejection_count": reset_rejection_count,
}

# 配置LLM客户端（从.env读取）
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL_ID = os.getenv("LLM_MODEL_ID")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

llm = OpenAICompatibleClient(model=MODEL_ID, api_key=API_KEY, base_url=BASE_URL)

# 初始化
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。
- `get_ticket_status(attraction_id="", attraction_name="", city="")`: 查询景点门票状态。
- `update_preferences(interest="", budget_min="", budget_max="")`: 更新用户的兴趣偏好和预算信息。
- `get_alternative_attractions(category="", original_id="", reason="sold_out")`: 当门票售罄或用户拒绝时，获取备选景点。reason可选"sold_out"或"rejected"。
- `refine_recommendation_strategy(rejection_pattern="")`: 在用户连续拒绝后调整推荐策略。
- `reset_rejection_count()`: 重置用户连续拒绝计数器。

# 交互方式：
- 如果你需要向用户提问（比如询问偏好、预算），使用 `ask_user("你的问题")`，系统会暂停等待用户输入。例如：Action: ask_user("请问您喜欢历史文化还是自然风光？预算大概多少？")
- 如果你发现用户对推荐不满意，或者用户输入中包含拒绝意图，使用 Action: user_rejected

# 对话流程：
1. 先用 get_weather 和 get_attraction 了解基本信息和推荐。
2. 用 ask_user 询问用户的兴趣偏好和预算，用户回答后调用 update_preferences 记录。
3. 如果想查询某个景点的门票，调用 get_ticket_status。
4. 如果门票售罄，系统会自动推荐备选方案。
5. 如果用户拒绝了推荐，记下 Action: user_rejected，系统会处理。
6. 如果用户连续拒绝了3次，系统会自动调整推荐策略。
7. 推荐时优先考虑用户的偏好和预算。

# 严格输出格式：
每次只输出一对：
Thought: [你的思考]
Action: [工具调用]

# 示例：
Thought: 用户想查询北京的天气。
Action: get_weather(city="北京")

开始吧！
"""

print(f"用户输入: {user_prompt}\n" + "=" * 40)

# 主循环
for i in range(5):
    print(f"--- 循环 {i + 1} ---\n")

    # 构建Prompt时加入用户记忆信息
    pref_summary = (
        f"[用户记忆] 兴趣偏好: {user_memory['preferences']}, "
        f"预算范围: {user_memory['budget_min']}-{user_memory['budget_max']}, "
        f"连续拒绝次数: {user_memory['rejection_count']}, "
        f"当前策略: {user_memory['last_strategy']}"
    )
    full_prompt = pref_summary + "\n" + "\n".join(prompt_history)

    # 调用LLM
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    match = re.search(
        r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
        llm_output,
        re.DOTALL,
    )
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)

    # 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "格式错误：你的回复必须包含 Action: 行。请重新以 Thought: ... Action: ... 格式输出。"
        print(f"解析错误: {observation}")
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    # 完成动作
    if action_str.startswith("finish"):
        final_answer = re.search(r'finish\(answer="(.*)"\)', action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        user_memory["rejection_count"] = 0
        break

    # 需要用户输入（如询问偏好）——输出 ask_user 消息
    if action_str.startswith("ask_user"):
        user_input_simulated = input(
            "【智能体需要您输入】"
            + action_str.replace("ask_user", "").strip('(")')
            + "\n请输入: "
        )
        observation = f"用户回复: {user_input_simulated}"
        if "历史文化" in user_input_simulated:
            update_preferences(interest="历史文化")
        elif "自然" in user_input_simulated:
            update_preferences(interest="自然风光")
        # 尝试解析预算
        import re as _re

        budget_match = _re.findall(r"(\d+)\s*[-~到]\s*(\d+)", user_input_simulated)
        if budget_match:
            update_preferences(
                budget_min=budget_match[0][0], budget_max=budget_match[0][1]
            )

    # 用户拒绝检测
    elif action_str.startswith("user_rejected"):
        user_memory["rejection_count"] += 1
        user_memory["interaction_count"] += 1
        print(f"用户拒绝了推荐（连续第{user_memory['rejection_count']}次）")

        if user_memory["rejection_count"] >= 3:
            print("检测到连续3次拒绝，触发推荐策略调整")
            observation = refine_recommendation_strategy(
                rejection_pattern=user_memory["preferences"]
            )
            user_memory["rejection_count"] = 0
        else:
            # 自动获取备选方案
            observation = get_alternative_attractions(
                category="general", reason="rejected"
            )
            if observation:
                alt_list = "\n".join(
                    [
                        f"- {a.name} (评分:{a.rating}, 价格:¥{a.price})"
                        for a in observation
                    ]
                )
                observation = f"用户拒绝了当前推荐（连续第{user_memory['rejection_count']}次）。备选推荐:\n{alt_list}"
            else:
                observation = f"用户拒绝了当前推荐，连续拒绝次数: {user_memory['rejection_count']}。"
    else:
        # 解析工具名称和参数
        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        if tool_name in available_tools:
            # 门票售罄检测与自动备选
            if tool_name == "get_ticket_status":
                ticket_result = available_tools[tool_name](**kwargs)
                if "售罄" in ticket_result or "sold_out" in ticket_result.lower():
                    # 自动推荐备选
                    category = kwargs.get("category", "general")
                    alternatives = get_alternative_attractions(
                        category=category,
                        original_id=kwargs.get("attraction_id", ""),
                        reason="sold_out",
                    )
                    if alternatives:
                        alt_text = "\n".join(
                            [
                                f"{i+1}. {a.name} (评分:{a.rating}, 价格:¥{a.price})"
                                for i, a in enumerate(alternatives)
                            ]
                        )
                        observation = (
                            f"{ticket_result}\n已为您推荐以下备选景点:\n{alt_text}"
                        )
                    else:
                        observation = f"{ticket_result}\n未找到合适的备选景点，您是否想看看其他类型的景点？"
                else:
                    observation = ticket_result
            else:
                observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "=" * 40)
    prompt_history.append(observation_str)
