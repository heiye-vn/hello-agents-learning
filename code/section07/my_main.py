import os
from pathlib import Path
from dotenv import load_dotenv

from my_llm import MyLLM

load_dotenv(Path(__file__).parent / ".env")

# 实例化重写的客户端，并指定 provider
# llm = MyLLM(provider="gemini")
llm = MyLLM(provider="modelscope")

messages = [{"role": "user", "content": "你好，请介绍一下自己。"}]

response_stream = llm.think(messages)

print("Gemini Response:")
for chunk in response_stream:
    # chunk在my_llm库中已经打印过一遍，这里只需要pass即可
    # print(chunk, end="", flush=True)
    pass
