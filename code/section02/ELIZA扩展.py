import re
import random

# 全局上下文记忆
user_context = {}

# 定义规则库
rules = {
    r"I need (.*)": [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?",
    ],
    r"Why don\'t you (.*)\?": [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?",
    ],
    r"Why can\'t I (.*)\?": [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?",
    ],
    r"I am (.*)": [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?",
    ],
    r".* mother .*": [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?",
    ],
    r".* father .*": [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?",
    ],
    r"I work (.*)": [
        "What do you like about being a {0}?",
        "How long have you worked as a {0}?",
        "Does being a {0} make you happy?",
    ],
    r"I study (.*)": [
        "Why did you choose to study {0}?",
        "What do you find most interesting about {0}?",
        "How do you feel when studying {0}?",
    ],
    r"My hobby is (.*)": [
        "How long have you been interested in {0}?",
        "What do you enjoy most about {0}?",
        "How does {0} make you feel?",
    ],
    r".*": [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?",
    ],
}

# 扩展代词转换
pronoun_swap = {
    "i": "you",
    "you": "i",
    "me": "you",
    "my": "your",
    "am": "are",
    "are": "am",
    "was": "were",
}


def swap_pronouns(phrase):
    """对输入短语中的代词进行转换"""
    if not phrase:
        return ""
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)


def update_context(user_input):
    """从输入中提取关键信息"""
    # 提取姓名
    if "my name is" in user_input.lower():
        match = re.search(r"my name is (.*)", user_input, re.IGNORECASE)
        if match:
            name = match.group(1).strip(" .,!?")
            if name and len(name.split()) <= 3:
                user_context["name"] = name
    if "i am " in user_input.lower():
        match = re.search(r"I am (.*)", user_input, re.IGNORECASE)
        if match:
            name = match.group(1).strip(" .,!?")
            if name and len(name.split()) <= 3:
                user_context["name"] = name
    # 提取年龄
    if "years old" in user_input.lower():
        match = re.search(r"(\d+) years? old", user_input, re.IGNORECASE)
        if match:
            user_context["age"] = match.group(1)

    # 提取职业
    if "work" in user_input.lower() and (
        " as " in user_input.lower() or "at " in user_input.lower()
    ):
        match = re.search(r"work (as|at) (.*)", user_input, re.IGNORECASE)
        if match:
            user_context["job"] = match.group(2).strip(" .,!?")


def get_personalized_response():
    """根据记忆生成个性化响应"""
    if not user_context:
        return ""

    responses = []
    if "name" in user_context:
        name = user_context["name"]
        responses.extend(
            [
                f"By the way {name}, ",
                f"{name}, I wanted to ask, ",
                f"Speaking of that {name}, ",
            ]
        )

    if "age" in user_context and "job" in user_context:
        responses.append(
            f"Being {user_context['age']} and a {user_context['job']} must be interesting. "
        )
    elif "age" in user_context:
        responses.append(f"At {user_context['age']} years old, ")
    elif "job" in user_context:
        responses.append(f"As a {user_context['job']}, ")

    return random.choice(responses) if responses else ""


def respond(user_input):
    """生成响应"""
    # 更新上下文记忆
    update_context(user_input)

    # 检查是否询问记忆中的信息
    if "what is my" in user_input.lower() or "do you remember" in user_input.lower():
        if "name" in user_input.lower() and "name" in user_context:
            return f"Your name is {user_context['name']}."
        elif "age" in user_input.lower() and "age" in user_context:
            return f"You are {user_context['age']} years old."
        elif (
            "job" in user_input.lower() or "work" in user_input.lower()
        ) and "job" in user_context:
            return f"You are a {user_context['job']}."

    # 检查是否提及姓名
    if "name" in user_context and user_context["name"].lower() in user_input.lower():
        responses = [
            f"You mentioned your name, {user_context['name']}. Tell me more.",
            f"{user_context['name']}, that's interesting. Please continue.",
            f"Go on, {user_context['name']}.",
        ]
        return random.choice(responses)

    # 正常规则匹配
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            captured_group = match.group(1) if match.groups() else ""
            if len(match.groups()) > 1:
                captured_group = match.group(2)

            swapped_group = swap_pronouns(captured_group)

            # 格式化响应
            if "{0}" in responses[0] or "{1}" in responses[0]:
                if "{1}" in responses[0] and len(match.groups()) >= 2:
                    response = random.choice(responses).format(
                        match.group(1), swapped_group
                    )
                else:
                    response = random.choice(responses).format(swapped_group)
            else:
                response = random.choice(responses)

            # 随机添加个性化内容
            if random.random() < 0.3:  # 30%概率添加个性化
                personalized = get_personalized_response()
                if personalized:
                    response = personalized + response.lower()

            return response

    return random.choice(rules[r".*"])


# 主聊天循环
if __name__ == "__main__":
    print("ELIZA with Memory: I can remember your name, age, and job.")
    print("Type 'quit' to exit.")
    print("-" * 40)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            if "name" in user_context:
                print(f"Therapist: Goodbye, {user_context['name']}!")
            else:
                print("Therapist: Goodbye!")
            break

        response = respond(user_input)
        print(f"Therapist: {response}")

        # 展示当前记忆
        if user_context and random.random() < 1:  # 20%概率展示记忆
            print(
                f"[I remember: {', '.join([f'{k}: {v}' for k, v in user_context.items()])}]"
            )
