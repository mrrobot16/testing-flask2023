from utils import generate_timestamp, generate_unique_id

class User:

    def __init__(self, db):
        self.db = db
        self.collection_ref = self.db.collection('users')

    def create(self, conversations=[]):
        self.user_id = generate_unique_id()  # Generate a unique 20-character ID
        self.created_at = generate_timestamp()  # Get current timestamp
        self.conversations = conversations  # Initialize with an empty array of conversation references
        
        user = {
            'id': self.user_id,
            'created_at': self.created_at,
            'conversations': self.conversations
        }
        
        user_ref = self.collection_ref.document(self.user_id)
        user_ref.set(user)
        return user_ref

    def get_all(self):
        
        users = self.collection_ref.stream()

        # Convert each DocumentSnapshot to a dictionary and add it to a list
        user_list = [user.to_dict() for user in users]
        return user_list