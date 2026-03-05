"""LLM 初始化（使用 LangChain 1.0+ API）"""

from langchain_openai import ChatOpenAI
from config.settings import settings


def get_llm():
    """获取 LLM 实例（基于配置）"""
    provider = settings.llm_provider.lower()

    # 所有提供商都使用 OpenAI 兼容接口
    # 包括：OpenAI、DeepSeek、阿里百炼、iFlow 等
    return ChatOpenAI(
        model=settings.llm_model_id,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
    )
