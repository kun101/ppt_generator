import httpx
import json as pyjson
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    name = "gemini"
    
    async def generate(self, prompt: str, system: str = "", json: bool = True) -> str:
        # Combine system and user prompts for Gemini
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        
        if json:
            full_prompt += "\n\nIMPORTANT: Respond with valid JSON only. Do not wrap in markdown code blocks or add any formatting. Return raw JSON directly."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4000
            }
        }
        
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload)
        
        # Log response for debugging
        print(f"DEBUG: Gemini HTTP status: {response.status_code}")
        print(f"DEBUG: Gemini response headers: {dict(response.headers)}")
        
        response.raise_for_status()
        result = response.json()
        
        print(f"DEBUG: Gemini raw response: {result}")
        
        # Validate response structure
        if "candidates" not in result:
            raise ValueError(f"No candidates in response: {result}")
        
        if not result["candidates"]:
            raise ValueError("Empty candidates list in response")
        
        candidate = result["candidates"][0]
        if "content" not in candidate:
            raise ValueError(f"No content in candidate: {candidate}")
        
        if "parts" not in candidate["content"]:
            raise ValueError(f"No parts in content: {candidate['content']}")
        
        if not candidate["content"]["parts"]:
            raise ValueError("Empty parts list in content")
        
        text_response = candidate["content"]["parts"][0].get("text", "")
        
        if not text_response.strip():
            raise ValueError("Empty text response from Gemini")
        
        print(f"DEBUG: Gemini text response: {text_response[:200]}...")
        
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
