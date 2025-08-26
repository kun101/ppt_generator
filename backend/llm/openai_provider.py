import httpx
import json as pyjson
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    name = "openai"
    
    async def generate(self, prompt: str, system: str = "", json: bool = True) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        if json:
            payload["response_format"] = {"type": "json_object"}
        
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers, 
                json=payload
            )
        
        response.raise_for_status()
        result = response.json()
        text_response = result["choices"][0]["message"]["content"]
        
        # Extract JSON from markdown code blocks if present
        cleaned_response = self._extract_json_from_markdown(text_response)
        
        return cleaned_response
    
    def _extract_json_from_markdown(self, text: str) -> str:
        """Extract JSON content from markdown code blocks."""
        import re
        
        # Look for JSON wrapped in markdown code blocks
        json_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        match = re.search(json_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            # Found JSON in code blocks, extract it
            json_content = match.group(1).strip()
            print(f"DEBUG: Extracted JSON from markdown: {json_content[:200]}...")
            return json_content
        else:
            # No code blocks found, return the original text
            print("DEBUG: No markdown code blocks found, returning original text")
            return text.strip()
