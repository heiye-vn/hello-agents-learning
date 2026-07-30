import os
from hello_agents import HelloAgentsLLM
from hello_agents.core.llm_adapters import OpenAIAdapter


class MyLLM(HelloAgentsLLM):
    """
    自定义 LLM 客户端，继承自 HelloAgentsLLM
    """

    # 重写 __init__ 方法以支持新供应商
    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        provider: str | None = "auto",
        **kwargs
    ):
        # 检查 provider 是否为我们想处理的 'modelscope'
        if provider == "modelscope":
            print("正在使用自定义的 ModelScope Provider")
            self.provider = "modelscope"

            # 解析 ModelScope 的凭证
            self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
            self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"

            # 验证凭证是否存在
            if not self.api_key:
                raise ValueError(
                    "ModelScope API Key 不存在，请检查配置文件或环境变量。"
                )

            # 设置默认模型和其它参数
            self.model = (
                model
                or os.getenv("MODELSCOPE_MODEL_ID")
                or "Qwen/Qwen2.5-VL-72B-Instruct"
            )
            self.temperature = kwargs.get("temperature", 0.7)
            self.max_tokens = kwargs.get("max_tokens")
            self.timeout = kwargs.get("timeout", 60)
            self.kwargs = kwargs
            self.last_call_stats = None

            # 创建适配器给 self._adapter
            self._adapter = OpenAIAdapter(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                model=self.model,
            )

        # 如果是 Gemini Provider，则添加相应的处理逻辑
        elif provider == "gemini":
            print("正在使用自定义的 Gemini Provider")

            self.provider = "gemini"

            # 读取 Gemini 专用环境变量
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            self.base_url = base_url or os.getenv(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/",
            )

            if not self.api_key:
                raise ValueError("Gemini API Key 不存在。请检查配置文件或环境变量。")

            # 模型参数
            self.model = model or os.getenv("GEMINI_MODEL_ID") or "gemini-1.5-flash"
            self.temperature = kwargs.get("temperature", 0.7)
            self.max_tokens = kwargs.get("max_tokens")
            self.timeout = kwargs.get("timeout", 60)
            self.kwargs = kwargs
            self.last_call_stats = None

            # 创建适配器给 self._adapter
            self._adapter = OpenAIAdapter(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                model=self.model,
            )

        else:
            # 如果不是以上的供应商，则使用父类的原始逻辑来处理
            super().__init__(model=model, api_key=api_key, base_url=base_url, **kwargs)


# ==================== my_llm.py 的最底部 ====================
if __name__ == "__main__":
    from pathlib import Path
    from dotenv import load_dotenv

    # 1. 自测时手动加载 .env
    load_dotenv(Path(__file__).parent / ".env")

    # 2. 测试实例化
    llm = MyLLM(provider="gemini")
    res = llm.think([{"role": "user", "content": "你当前是什么模型"}])
    for chunk in res:
        pass
