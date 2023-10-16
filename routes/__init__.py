from flask import jsonify
from config import FIREBASE_CREDENTIALS
allowed_origins = ['https://irs-copilot.vercel.app/', 'https://irs-copilot.vercel.app', 'http://localhost:3000']

def register(app):
    @app.route('/')
    def health():
        return jsonify({'status': 'ok', 'FIREBASE_CREDENTIALS': FIREBASE_CREDENTIALS})

    return app