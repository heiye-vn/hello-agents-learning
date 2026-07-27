import ollama


# 定义调参调用的函数
def query_model(prompt: str):
    response = ollama.chat(
        model="qwen3:0.6b",  # 指定本地部署的模型名称
        messages=[
            {
                "role": "system",
                "content": "你是一个严谨的技术专家。如果不知道答案请明确告知，禁止编造事实",  # 系统提示词约束
            },
            {"role": "user", "content": prompt},  # 用户输入
        ],
        # ⚙️ 关键词调参区域：控制输出的准确性与随机性
        options={
            "temperature": 0.1,  # 采样温度，越低越严谨稳定；越高越具创造性但易幻觉（默认为 0.7）
            "top_p": 0.9,  # 采样累积概率控制
            "seed": 42,  # 随机种子：固定后相同的输入每次输出完全一致，便于对比验证
            "num_ctx": 4096,  # 上下文窗口 Token 大小
        },
    )
    return response["message"]["content"]


# 测试调用
answer = query_model("请简述什么是 JWT，并说明其优缺点。")
print(answer)
