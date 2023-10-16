from constants.openai import OPENAI_USER_PROMPT, OPENAI_ENGINE
from models.openai import OpenAI

def chat_completion(prompt, engine = OPENAI_ENGINE):
    openai = OpenAI(engine) if engine else OpenAI()
    openai_response = openai.chat_completion(prompt)
    return openai_response