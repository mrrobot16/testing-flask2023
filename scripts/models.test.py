from models import User, Conversation, Message
from firebase import firestore_db, firestore

def create_user():
    user = User(firestore_db)
    return user.new()

def create_conversation(user_id):
    conversation = Conversation(firestore_db)
    return conversation.create(user_id)

def create_message(user_id, conversation_id, content, role):
    message = Message(firestore_db, user_id, conversation_id)
    return message.create(user_id, conversation_id, content, role)

def update_user(id, email):
    user = User(firestore_db)
    return user.update(id, email)

def activate_user(id):
    user = User(firestore_db)
    return user.activate(id)

def deactivate_user(id):
    user = User(firestore_db)
    return user.deactivate(id)

def delete_user(id):
    user = User(firestore_db)
    return user.delete(id)

# Create User
user = create_user()
# user_id = user.get().to_dict().get('id')
user_id = user['id']
print('user_id', user_id)

conversation = create_conversation(user_id)
# conversation_id = conversation.get().to_dict().get('id')
conversation_id = conversation
print('conversation_id', conversation_id)

content = 'Hello Jarvis, what is a 1099?'
role = 'user'
message = create_message(user_id, conversation_id, content, role)
# message = create_message(existing_user_id, conversation_id, content, role)
# message_id = message.get().to_dict().get('id')
message_id = message
print('message_id', message_id)

# NOTE: Below are harded coded existing user id for testing update and delete methods.
# existing_user_id = 'b51ccb22-ed74-4bd2-8'
existing_user_id = '79047852-cdf3-47d4-b'
# existing_user_id = ''
print('existing_user_id', existing_user_id)

# Update User
email = 'hector@gmail.com'
user = update_user(existing_user_id, email)
print('updated_user', user)

# Deactivate User
deactivated_user = deactivate_user(existing_user_id)
print('deactivated_user', deactivated_user)

# Activate User
activated_user = activate_user(existing_user_id)
print('activated_user', activated_user)

# Delete User
# deleted_user = delete_user(existing_user_id)
# delete_user_id = delete_user
# print("deleted_user_id", delete_user)

