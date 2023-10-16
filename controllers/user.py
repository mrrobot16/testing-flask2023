from flask import Blueprint, jsonify, request
from services.user import get_users, new_user, get_user, update_user, delete_user, deactivate_user, activate_user

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/health', methods=['GET'])
def health():
    response = {
        'status': 'ok'
    }
    return jsonify(response)

@user_controller.route('/', methods=['GET'])
def get_all():
    response = {
        'status': 200, 
        'data': get_users()
    }
    return jsonify(response)

@user_controller.route('/<id>', methods=['GET'])
def get(id):
    response = {
        'status': 200, 
        'data': get_user(id)
    }
    return jsonify(response)

@user_controller.route('/new', methods=['POST'])
def new():
    email = request.get_json()['email']
    password = request.get_json()['password']
    response = {
        'status': 200, 
        'data': new_user(email, password)
    }
    return jsonify(response)

@user_controller.route('/update/<id>', methods=['PUT'])
def update(id):
    email = request.get_json()['email']
    # password = request.get_json()['password']
    response = {
        'status': 200, 
        'data': update_user(id, email)
    }
    return jsonify(response)

@user_controller.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    response = {
        'status': 200,
        'data': delete_user(id)
    }
    return jsonify(response)

@user_controller.route('/activate/<id>', methods=['PUT'])
def activate(id):
    response = {
        'status': 200, 
        'data': activate_user(id)
    }
    return jsonify(response)

@user_controller.route('/deactivate/<id>', methods=['PUT'])
def deactivate(id):
    response = {
        'status': 200, 
        'data': deactivate_user(id)
    }
    return jsonify(response)
