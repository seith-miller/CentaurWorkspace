from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


def get_llm_provider(provider: str, model: str):
    if provider == "openai":
        return OpenAIProvider(model=model)
    elif provider == "anthropic":
        return AnthropicProvider(model=model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
