from flask import Blueprint, jsonify, request
from services.openai import chat_completion
from constants.openai import OPENAI_ENGINE, OPENAI_CHAT_COMPLETION_ENDPOINT_ERROR

# # Create a blueprint instance
openai_controller = Blueprint('openai_controller', __name__)

# Define routes using the blueprint
@openai_controller.route('/health')
def health():
    return jsonify({'status': 'ok'})

@openai_controller.route('/chat-completion', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', None)
    engine = data.get('engine', None)
    if prompt is None:
        error = OPENAI_CHAT_COMPLETION_ENDPOINT_ERROR, OPENAI_CHAT_COMPLETION_ENDPOINT_ERROR['status_code']
        return jsonify(error)
    else:
        response = chat_completion(prompt, engine)
        return jsonify({'response': response})