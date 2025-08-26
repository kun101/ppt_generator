from typing import Dict, Any

class LLMProvider:
    name: str
    
    def __init__(self, api_key: str): 
        self.api_key = api_key
    
    async def generate(self, prompt: str, system: str = "", json: bool = True) -> str:
        raise NotImplementedError("Subclasses must implement generate method")
