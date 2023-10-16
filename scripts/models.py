import uuid
from datetime import datetime
from firebase import firestore
from utils import generate_unique_id, generate_timestamp, hash_password
import warnings

class User:

    def __init__(self, db):
        self.db = db # Reference to the Firestore database
        self.collection_ref = self.db.collection('users') # Reference to the 'users' collection
        self.id = None # string
        self.conversations = None # array of conversation reference
        self.email = None # string
        self.password = None # string
        self.active = True
        self.auth_type = 'email-password'
        self.created_at = None # timestamp
        self.updated_at = None # timestamp

    def get_all(self):
        users = self.collection_ref.stream()

        # Convert each DocumentSnapshot to a dictionary and add it to a list
        user_list = [user.to_dict() for user in users]
        return user_list

    def get(self, id):
        # NOTE: Suppress "Prefer using the 'filter' keyword argument instead." warning.
        # This happens when using collection_ref.where()
        warnings.filterwarnings("ignore", category=UserWarning, message="Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.")

        # Query the collection where 'id' is equal to user_id
        users = self.collection_ref.where('id', '==', id).limit(1).stream()

        # Users is an iterator of DocumentSnapshot
        # Converting DocumentSnapshot to a dictionary

        user_list = [user.to_dict() for user in users]
        # NOTE: collection_ref.where returns an array of documents.
        # We only want the first document in the array.
        return user_list[0]

    def new(self, email = None, password = None, conversations = []):
        self.id = generate_unique_id()  # Generate a unique 20-character ID
        self.email = email
        # self.password = hash_password(self.email) # NOTE: This is a placeholder for now.
        self.conversations = conversations  # Initialize with an empty array of conversation references
        self.created_at = generate_timestamp()  # Get current timestamp
        self.updated_at = self.created_at
        user = {
            'id': self.id,
            'email': self.email,
            # 'password': str(self.password),
            'conversations': self.conversations,
            'active': self.active,
            'auth_method': self.auth_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        # NOTE: Add the user to the 'users' collection
        user_ref = self.collection_ref.document(self.id)
        user_ref.set(user)
        # NOTE: return user object versus firebase user reference to reduce the amount of reads/writes.
        return user['id'] 

    def update(self, id, email, password = None):
        self.id = id
        self.email = email
        # self.password = hash_password(password) if password else hash_password(self.email)
        self.updated_at = generate_timestamp()
        user = {
            'id': self.id,
            'email': self.email,
            # 'password': str(self.password),
            'updated_at': self.updated_at
        }

        # NOTE: Here, you can use the set method with merge=True to update or create if the document doesn't exist
        users_ref = self.collection_ref.document(self.id)
        users_ref.set(user, merge=True)
        return user

    def activate(self, id):
        self.id = id
        self.active = True
        user = {
            'id': self.id,
            'active': self.active
        }

        users_ref = self.collection_ref.document(self.id)
        users_ref.set(user, merge=True)
        return user

    def deactivate(self, id):
        self.id = id
        self.active = False
        user = {
            'id': self.id,
            'active': self.active
        }

        users_ref = self.collection_ref.document(self.id)
        users_ref.set(user, merge=True)
        return user

    def delete(self, id):
        self.id = id
        user = {
            'id': self.id
        }

        users_ref = self.collection_ref.document(self.id)
        users_ref.delete()
        return user

class Conversation:

    def __init__(self, db):
        self.db = db
        self.collection_ref = self.db.collection('conversations')
        self.user_collection_ref = self.db.collection('users')

    def create(self, user_id, messages = []):
        # NOTE: 
        # This will change based on the context of the conversation.
        self.id = generate_unique_id()
        self.created_at = generate_timestamp()
        self.name = f'New conversation id:{self.id[0:2]}'
        self.user_id = user_id
        self.messages = messages

        conversation = {
            'name': self.name,
            'id': self.id,
            'created_at': self.created_at,
            'messages': self.messages,
            'user_id': self.user_id
        }
        
        conversation_ref = self.collection_ref.document(self.id)
        conversation_ref.set(conversation)

        user_ref = self.user_collection_ref.document(self.user_id)
        user_ref.update({
        'conversations': firestore.ArrayUnion([conversation_ref])
        })

        # return conversation_ref
        return self.id

class Message:

    def __init__(self, db, user_id, conversation_id):
        self.db = db
        self.collection_ref = self.db.collection('messages')


    def create(self, user_id, conversation_id, content, role):

        self.id = generate_unique_id()
        self.created_at = generate_timestamp()
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.content = content
        self.role = role

        message = {
            'id': self.id,
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'created_at': self.created_at,
            'content': self.content,
            'role': self.role # role can only be 'system', 'assistant' or 'user' 
        }

        message_ref = self.collection_ref.document(self.id)
        message_ref.set(message)

        conversation_ref = self.db.collection('conversations').document(self.conversation_id)
        conversation_ref.update({
            'messages': firestore.ArrayUnion([message_ref])
        })

        return message.id