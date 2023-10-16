import uuid
from datetime import datetime
import bcrypt

# Generate a unique ID
def generate_unique_id(size=20):
    return str(uuid.uuid4())[:size]

# Set current timestamp
def generate_timestamp():
    return datetime.utcnow()

def methods_and_attributes(obj):
    print("Methods of the object:")
    for item in dir(obj):
        if callable(getattr(obj, item)):
            print(item)

# Generate a salt & Hash the password along with the salt
def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password

# Check the provided password against the hashed one
def verify_hashed_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


# methods_and_attributes = dir(user)

# print("Methods of the object:")
# for item in methods_and_attributes:
#     if callable(getattr(user, item)):
#         print(item)