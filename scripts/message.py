from utils import generate_timestamp, generate_unique_id
from db.firebase import firestore

from utils import generate_timestamp, generate_unique_id

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

        return message_ref