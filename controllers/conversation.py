from flask import Blueprint, jsonify, request
from services.conversation import get_conversations, get_conversation, new_conversation, update_conversation, deactivate_conversation, delete_conversation, get_conversations_by_user, new_message, new_message_to_openai, new_conversation_with_openai

conversation_controller = Blueprint('conversation_controller', __name__)

@conversation_controller.route('/health', methods=['GET'])
def health():
    response = {
        'status': 'ok'
    }
    return jsonify(response)

@conversation_controller.route('/', methods=['GET'])
def get_all():
    response = {
        'status': 200, 
        'data': get_conversations()
    }
    return jsonify(response)

@conversation_controller.route('/user/<user_id>', methods=['GET'])
def get_all_by_user(user_id):
    response = {
        'status': 200, 
        'data': get_conversations_by_user(user_id)
    }
    return jsonify(response)

@conversation_controller.route('/<id>', methods=['GET'])
def get(id):
    response = {
        'status': 200, 
        'data': get_conversation(id)
    }
    return jsonify(response)

@conversation_controller.route('/new', methods=['POST'])
def new():
    user_id = request.get_json()['user_id']
    response = {
        'status': 200, 
        'data': new_conversation(user_id)
    }
    return jsonify(response)

@conversation_controller.route('/new/openai', methods=['POST'])
def new_conversation_openai():
    user_id = request.get_json()['user_id']
    message = request.get_json()['message']
    data = new_conversation_with_openai(user_id, message)
    response = {
        'status': 200, 
        'conversation': data['conversation'],
        'openai_message': data['openai_message'],
        'user_message': data['user_message']
    }
    return jsonify(response)

@conversation_controller.route('/message/new/<id>', methods=['POST'])
def new_conversation_message(id):
    user_id = request.get_json()['user_id']
    message = request.get_json()['message']
    response = {
        'status': 200, 
        'data': new_message(user_id, id, message)
    }
    return jsonify(response)

@conversation_controller.route('/message/new/openai/<id>', methods=['POST'])
def new_conversation_message_to_openai(id):
    user_id = request.get_json()['user_id']
    message = request.get_json()['message']
    data = new_message_to_openai(user_id, id, message)
    response = {
        'status': 200, 
        'conversation_id': data['conversation_id'],
        'openai_message': data
    }
    return jsonify(response)

@conversation_controller.route('/update/<id>', methods=['PUT'])
def update(id):
    name = request.get_json()['name']
    response = {
        'status': 200, 
        'data': update_conversation(id, name)
    }
    return jsonify(response)

@conversation_controller.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    response = {
        'status': 200,
        'data': delete_conversation(id)
    }
    return jsonify(response)

@conversation_controller.route('/deactivate/<id>', methods=['PUT'])
def deactivate(id):
    response = {
        'status': 200, 
        'data': deactivate_conversation(id)
    }
    return jsonify(response)

# @conversation_controller.route('/delete/<id>', methods=['DELETE'])
# def delete(id):
#     response = {
#         'status': 200,
#         'data': delete_conversation(id)
#     }
#     return jsonify(response)

