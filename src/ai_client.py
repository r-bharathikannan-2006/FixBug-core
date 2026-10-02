import os
from google import genai
from google.genai import types
from tenacity import retry, wait_exponential, stop_after_attempt
import ollama

def get_installed_ollama_models(host: str = "http://localhost:11434") -> list[str]:
    """Queries the local Ollama service to retrieve a list of all downloaded model tags."""
    try:
        client = ollama.Client(host=host.rstrip('/'))
        response = client.list()
        models = []
        
        model_items = getattr(response, 'models', None)
        if model_items is None and isinstance(response, dict):
            model_items = response.get('models', [])
            
        if model_items:
            for item in model_items:
                if hasattr(item, 'model'):
                    models.append(item.model)
                elif isinstance(item, dict):
                    models.append(item.get('model') or item.get('name'))
                elif isinstance(item, str):
                    models.append(item)
                    
        return [m for m in models if m]
    except Exception:
        return []


class GeminiClient:
    """Client wrapper for persistent chat sessions using the Google genai SDK."""
    def __init__(self, system_instruction: str, api_key: str, model: str):
        if not api_key:
            raise ValueError("Gemini API Key is missing. Please set it in settings.")
        
        self.client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                )
            ]
        )
        self.chat = self.client.chats.create(
            model=model, 
            config=config
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5),
        reraise=True
    )
    def send_message(self, message: str) -> str:
        response = self.chat.send_message(message)
        return response.text


class OllamaClient:
    """Client wrapper for persistent multi-turn chat sessions using Ollama local models."""
    def __init__(self, system_instruction: str, model: str, host: str = "http://localhost:11434"):
        if not model:
            raise ValueError("Ollama model is missing. Please configure model in settings.")
        
        self.model = model
        self.host = host.rstrip('/')
        self.client = ollama.Client(host=self.host)
        
        self.messages = []
        if system_instruction:
            self.messages.append({'role': 'system', 'content': system_instruction})

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    def send_message(self, message: str) -> str:
        self.messages.append({'role': 'user', 'content': message})
        try:
            response = self.client.chat(
                model=self.model,
                messages=self.messages
            )
            content = getattr(response.message, 'content', None) or response['message']['content']
            self.messages.append({'role': 'assistant', 'content': content})
            return content
        except Exception as e:
            self.messages.pop()
            if "not found" in str(e).lower():
                raise RuntimeError(
                    f"Model '{self.model}' was not found on your local Ollama server. "
                    f"Run 'ollama pull {self.model}' in your terminal."
                ) from e
            raise e


def create_ai_client(config: dict, system_instruction: str):
    """Factory function to instantiate the selected AI provider wrapper."""
    provider = config.get("provider", "gemini").lower()
    
    if provider == "ollama":
        return OllamaClient(
            system_instruction=system_instruction,
            model=config.get("ollama_model", "qwen2.5-coder"),
            host=config.get("ollama_host", "http://localhost:11434")
        )
    else:
        return GeminiClient(
            system_instruction=system_instruction,
            api_key=config.get("api_key", ""),
            model=config.get("model", "gemini-3.6-flash")
        )