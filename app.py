from flask import Flask, jsonify
from flask_cors import CORS

from routes import register, allowed_origins
from utils import log_firebase_credentials

log_firebase_credentials()
def create_app(config_name='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_name)
    CORS(app, origins = allowed_origins)
    return register(app)


app = create_app()

if __name__ == "__main__":
    app.run()