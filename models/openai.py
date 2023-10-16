import openai
from config import OPENAI_API_KEY_DEV
from constants.openai import OPENAI_ENGINE, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, OPENAI_ASSISTANT_PROMPT, OPENAI_SYSTEM_PROMPT, OPENAI_USER_PROMPT
from utils import generate_timestamp, generate_unique_id
class OpenAI:

    def __init__(self, engine = OPENAI_ENGINE, keys = OPENAI_API_KEY_DEV, temperature = OPENAI_TEMPERATURE,  max_tokens = OPENAI_MAX_TOKENS):
        self.id = generate_unique_id()
        self.keys = keys
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = self.keys

    def chat_completion(self, user_prompt = OPENAI_USER_PROMPT['content'], system_prompt = OPENAI_SYSTEM_PROMPT, assistant_prompt = OPENAI_ASSISTANT_PROMPT): 
        self.created_at = generate_timestamp()
        user_prompt = user_prompt.encode(encoding = 'ASCII', errors = 'ignore').decode()
        try:
            openai_response = openai.ChatCompletion.create(
                model = self.engine,
                messages = [
                    system_prompt,
                    assistant_prompt,
                    { "role": "user", "content": user_prompt }
                ],
                temperature = self.temperature,
                max_tokens = self.max_tokens
            )
            openai_response = OpenAIResponse(openai_response).to_dict()
            content = openai_response['choices'][0]['message']['content']
            role = openai_response['choices'][0]['message']['role']
            response = {
                "api": {
                    "id": self.id,
                    "created_at": self.created_at,
                    "prompt": user_prompt,
                    "content": content,
                    "role": role,
                },
                "openai": openai_response 
            }
            return response
        except Exception as error:
            return f"chat_completion error: {error}"

class OpenAIResponse:
    def __init__(self, response):
        self.id = response['id'] # str ie: "chatcmpl-89jaHxop3jAcGGTzeSZhpoJzP1g0y"
        self.object = response['object'] # str ie: "chat.completion"
        self.created = response['created'] # int ie: 1697330869
        self.model = response['model'] # str ie: "gpt-4"
        self.choices = response['choices'] # array [ { index: int, message: { role: str ie: assistant, content: str }, finish_reason: str } ]
        self.usage = response['usage'] # dict { prompt_tokens: int, completion_tokens: int, total_tokens: int }

    def to_dict(self):
        return {
            "id": self.id,
            "object": self.object,
            "created": self.created,
            "model": self.model,
            "choices": self.choices,
            "usage": self.usage
        }