from utils import generate_timestamp, generate_unique_id
from db.firebase import firestore
from models.message import Message, MessageGroup
import warnings

class Conversation:

    def __init__(self, db, convesation_id = None):
        self.db = db
        self.collection_ref = self.db.collection('conversations')
        self.user_collection_ref = self.db.collection('users')
        self.messages = [] # Array of Messages
        self.active = True # boolean
        self.created_at = None # timestamp
        self.updated_at = None # timestamp

    def get_all(self):
        conversations = self.collection_ref.stream()

        # Convert each DocumentSnapshot to a dictionary and add it to a list
        conversation_list = [conversation.to_dict() for conversation in conversations]
        return conversation_list

    def get_all_by_user(self, user_id):
        # NOTE: Suppress "Prefer using the 'filter' keyword argument instead." warning.
        # This happens when using collection_ref.where()
        message = "Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead."
        warnings.filterwarnings("ignore", category=UserWarning, message=message)

        conversations = self.collection_ref.where('user_id', '==', user_id).stream()
        conversation_list = [conversation.to_dict() for conversation in conversations]
        return conversation_list

    def get(self, id):
        # NOTE: Suppress "Prefer using the 'filter' keyword argument instead." warning.
        # This happens when using collection_ref.where()
        message = "Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead."
        warnings.filterwarnings("ignore", category=UserWarning, message=message)

        conversations = self.collection_ref.where('id', '==', id).limit(1).stream()
        conversation_list = [conversation.to_dict() for conversation in conversations]
        return conversation_list[0] if conversation_list else None

    def new(self, user_id):
        self.id = generate_unique_id()
        # NOTE: User id of the user who created the conversation.
        self.user_id = user_id 
        # NOTE: This will change based on the context of the conversation.
        self.name = f'Conversation #:{self.id[0:2]}'
        self.created_at = generate_timestamp()
        self.updated_at = self.created_at

        conversation = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'messages': self.messages,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        conversation_ref = self.collection_ref.document(self.id)
        conversation_ref.set(conversation)

        user_ref = self.user_collection_ref.document(self.user_id)
        user_ref.update({
        'conversations': firestore.ArrayUnion([conversation_ref])
        })

        return conversation

    def new_message(self, user_id, conversation_id, message):
        message = Message(user_id, conversation_id, message['content'], message['role'])
       
        conversation_ref = self.collection_ref.document(message.to_dict()['conversation_id'])
        conversation_ref.update({
            'messages': firestore.ArrayUnion([message.to_dict()])
        })

        conversation_ref.update({
            'updated_at': generate_timestamp()
        })

        return message.to_dict()
    
    def new_message_group(self, user_id, conversation_id, messages):
        message_group = MessageGroup(user_id, conversation_id, messages)
        return message_group.to_dict()

    def update(self, id, name):
        self.id = id
        self.name = name
        self.updated_at = generate_timestamp()
        conversation = {
            'id': self.id,
            'name': self.name,
            'updated_at': self.updated_at
        }
        conversation_ref = self.collection_ref.document(self.id)
        conversation_ref.set(conversation, merge=True)
        return conversation

    def deactivate(self, id):
        self.id = id
        self.active = False

        conversation = {
            'id': self.id,
            'active': self.active
        }
        conversation_ref = self.collection_ref.document(self.id)
        conversation_ref.set(conversation, merge=True)
        return conversation
    
    def delete(self, id):
        self.id = id

        conversation = {
            'id': self.id
        }
        conversation_ref = self.collection_ref.document(self.id)
        conversation_ref.delete()
        return conversation