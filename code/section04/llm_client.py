import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


# 加载当前脚本所在目录的 .env 文件
load_dotenv(Path(__file__).parent / ".env")


class HelloAgentsLLM:
    """
    封装 LLM 客户端。用于调用任何兼容 OpenAI 接口的服务，并默认使用流式响应
    """

    def __init__(
        self,
        model: str = None,
        apiKey: str = None,
        baseUrl: str = None,
        timeout: int = None,
    ):
        """初始化客户端，优先使用传入参数，如果未提供，则从环境变量加载。"""
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        raw_timeout = timeout or os.getenv("LLM_TIMEOUT", 60)
        try:
            self.timeout = float(raw_timeout)
        except (ValueError, TypeError):
            self.timeout = 60.0

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须提供或在.env文件中配置")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=self.timeout)

    def think(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0,
        show_reasoning: bool = False,
    ) -> str:
        """调用大语言模型进行思考，并返回其响应。

        参数:
        - messages: 消息列表
        - temperature: 采样温度
        - show_reasoning: 是否输出DeepSeek/R1等模型的深度思考过程 (reasoning_content)
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            reasoning_started = False

            for chunk in response:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta

                # 支持 DeepSeek / R1 等模型的深度思考/推理过程 (reasoning_content)
                if show_reasoning:
                    reasoning = getattr(delta, "reasoning_content", None)
                    if reasoning:
                        if not reasoning_started:
                            print("💭 [思考过程]: ", end="", flush=True)
                            reasoning_started = True
                        print(reasoning, end="", flush=True)

                # 处理模型正文回答 (content)
                content = delta.content or ""
                if content:
                    if show_reasoning and reasoning_started:
                        print("\n\n💬 [回答]: ", end="", flush=True)
                        reasoning_started = False
                    print(content, end="", flush=True)
                    collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            if hasattr(e, "__cause__") and e.__cause__:
                print(f"   底层原因: {e.__cause__}")
            print("\n💡 常见排查方法：")
            print(
                "1. 【网络/代理问题】：如果开启了 Clash / VPN / 代理工具，请尝试切换为【全局代理】或【直连】模式，或检查代理端口；"
            )
            print(
                f"2. 【配置问题】：请检查 .env 文件中的 LLM_BASE_URL ({os.getenv('LLM_BASE_URL')}) 是否可达；"
            )
            print(
                "3. 【API服务开销】：第三方 API 节点可能存在短时间断流，可再次运行或更换 Base URL。"
            )
            return None

    def think_with_reasoning(
        self, messages: List[Dict[str, str]], temperature: float = 0
    ) -> str:
        """显式打印思考过程 (reasoning_content) 的调用方法。"""
        return self.think(messages, temperature=temperature, show_reasoning=True)


# ===================== 添加主程序，验证 LLM 客户端 =====================

if __name__ == "__main__":
    try:
        llmClient = HelloAgentsLLM()
        exampleMessages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that writes Python code.",
            },
            {"role": "user", "content": "写一个快速排序算法"},
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)
