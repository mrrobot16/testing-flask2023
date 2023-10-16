from models.user import User
from db.firebase import firestore_db, firestore
from utils.firebase import convert_doc_refs

user = User(firestore_db)

def get_users():
    users = user.get_all()
    return convert_doc_refs(users)

def new_user(email, password):
    return user.new(email)

def get_user(id):
    user_by_id = user.get(id)
    return convert_doc_refs(user_by_id)

def update_user(id, email, password = None):
    return user.update(id, email, password)

def delete_user(id):
    return user.delete(id)

def deactivate_user(id):
    return user.deactivate(id)

def activate_user(id):
    return user.activate(id)