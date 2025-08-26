from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider

def get_provider(name: str, api_key: str):
    name = name.lower()
    if name == "openai": 
        return OpenAIProvider(api_key)
    elif name == "gemini": 
        return GeminiProvider(api_key)
    else:
        raise ValueError(f"Unsupported provider: {name}")
