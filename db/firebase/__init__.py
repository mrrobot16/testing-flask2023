import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from config import FIREBASE_CREDENTIALS

# Initialize Firebase Admin SDK
# credentials = credentials.Certificate("./credentials/firebase/irscopilot_dev-72ar9-0b73aebc83.json")
credentials = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(credentials)

client = firestore.client()

# Firestore database instance
firestore_db  = client