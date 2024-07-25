from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


def get_llm_provider(provider: str = None):
    if provider == "openai":
        return OpenAIProvider()
    elif provider == "anthropic":
        return AnthropicProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
