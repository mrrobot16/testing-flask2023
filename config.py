import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_ENV = os.environ.get('APP_ENV')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_GPT4_API_KEY = os.getenv("OPENAI_GPT4_API_KEY")

OPENAI_GPT3_API_KEY = os.getenv("OPENAI_GPT3_API_KEY")

OPENAI_API_KEY_PROD = os.getenv("OPENAI_API_KEY_PROD")

OPENAI_API_KEY_DEV = os.getenv("OPENAI_API_KEY_DEV")

TESTING = True

DEBUG = True

FIREBASE_CREDENTIALS = {
    'type': os.getenv('TYPE'),
    'project_id': os.getenv('PROJECT_ID'),
    'private_key_id': os.getenv('PRIVATE_KEY_ID'),
    'private_key': os.getenv('PRIVATE_KEY'),
    'client_email': os.getenv('CLIENT_EMAIL'),
    'client_id': os.getenv('CLIENT_ID'),
    'auth_uri': os.getenv('AUTH_URI'),
    'token_uri': os.getenv('TOKEN_URI'),
    'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL'),
    'universe_domain': os.getenv('UNIVERSE_DOMAIN')
}