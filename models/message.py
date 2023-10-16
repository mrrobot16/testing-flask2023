from utils import generate_timestamp, generate_unique_id
from db.firebase import firestore

class Message:

    def __init__(self, user_id, conversation_id, content, role):
        self.id = generate_unique_id()
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.content = content
        self.role = role
        self.created_at = generate_timestamp()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "role": self.role,
            "created_at": self.created_at
        }

class MessageGroup:
    def __init__(self, user_id, conversation_id,  messages):
        self.id = generate_unique_id()
        self.user_id = user_id
        self.conversation_id = conversation_id
        # NOTE: For now self.messages will only be a list of 1 prompt Message and 1 response Message.
        self.messages = [messages[0], messages[1]] # Message[]
        self.created_at = generate_timestamp()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "messages": self.messages
        }
