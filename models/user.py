from utils import generate_timestamp, generate_unique_id, hash_password, verify_hashed_password
from models.conversation import Conversation
import warnings

class User:

    def __init__(self, db):
        self.db = db # Reference to the Firestore database
        self.collection_ref = self.db.collection('users') # Reference to the 'users' collection
        self.id = None # string
        self.conversations = None # array of conversation reference
        self.email = None # string
        self.password = None # string
        self.active = True # boolean
        self.auth_type = 'email-password' # string ['google, apple, github, etc]
        self.created_at = None # timestamp
        self.updated_at = None # timestamp

    def get_all(self):
        users = self.collection_ref.stream()

        # Convert each DocumentSnapshot to a dictionary and add it to a list
        user_list = [user.to_dict() for user in users]
        return user_list

    def get(self, id):
        # Suppress "Prefer using the 'filter' keyword argument instead." warning.
        # This happens when using collection_ref.where()
        warnings.filterwarnings("ignore", category=UserWarning, message="Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.")

        # Query the collection where 'id' is equal to user_id
        users = self.collection_ref.where('id', '==', id).limit(1).stream()

        # Users is an iterator of DocumentSnapshot
        # Converting DocumentSnapshot to a dictionary

        user_list = [user.to_dict() for user in users]
        # NOTE: collection_ref.where returns an array of documents.
        # We only want the first document in the array.

        return user_list[0] if user_list else None

    def new(self, email = None, password = None, conversations = []):
        self.id = generate_unique_id()  # Generate a unique 20-character ID
        self.email = email
        self.password = hash_password(email) # NOTE: This is a placeholder for now.
        self.conversations = conversations  # Initialize with an empty array of conversation references
        self.created_at = generate_timestamp()  # Get current timestamp
        self.updated_at = self.created_at

        user = {
            'id': self.id,
            'email': self.email,
            'password': str(self.password),
            'conversations': self.conversations,
            'active': self.active,
            'auth_method': self.auth_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        # Add the user to the 'users' collection
        user_ref = self.collection_ref.document(self.id)
        user_ref.set(user)
        return user # return user object versus firebase user reference to reduce the amount of reads/writes.

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
        # Here, you can use the set method with merge=True to update or create if the document doesn't exist
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
        # Here, you can use the set method with merge=True to update or create if the document doesn't exist
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
