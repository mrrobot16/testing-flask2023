from utils import generate_timestamp, generate_unique_id, convert_doc_ref_to_serializable
from db.firebase import firestore

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

        return conversation_ref
    
    # def get_by_id(self, conv_id):
    #     # Retrieve a document by ID and convert it to a dictionary
    #     conversation_ref = self.collection_ref.document(conv_id)
    #     conversation = conversation_ref.get()
    #     if conversation.exists:
    #         conversation_dict = conversation.to_dict()

    #         return conversation_dict
    #     else:
    #         return None  # or handle the case where the conversation does not exist as appropriate


    def get_by_id(self, conv_id):
        conversation_ref = self.collection_ref.document(conv_id)
        conversation = conversation_ref.get()
        if conversation.exists:
            conversation_dict = conversation.to_dict()

            # If there are any DocumentReferences in the conversation, convert them here
            # For example:
            if 'messages' in conversation_dict:
                conversation_dict['messages'] = convert_doc_ref_to_serializable(conversation_dict['messages'])

            return conversation_dict
        else:
            return None