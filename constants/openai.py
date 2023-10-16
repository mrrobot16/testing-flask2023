OPENAI_SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful tax CPA for the United States of America with experience working with the IRS."
}

OPENAI_ASSISTANT_PROMPT = {
    "role": "assistant",
    "content": "I will respond all IRS related questions based on the forms that exist on the IRS website. Please type your question."
}

OPENAI_USER_PROMPT = {
    "role": "user",
    "content": "Tell me about the IRS and the possible forms."
}

OPENAI_ENGINE = 'gpt-3.5-turbo-16k'
OPENAI_TEMPERATURE = 0.5
OPENAI_MAX_TOKENS = 1000

OPENAI_CHAT_COMPLETION_ENDPOINT_ERROR  = { 
    'message': "Missing prompt and engine in the request",
    'status_code': 400
}