import os
import json
from dotenv import load_dotenv

load_dotenv()

# SERVER CONFIGS
PORT = int(os.getenv("PORT", "8010"))
MAX_POOL = int(os.getenv("MAX_POOL", "12"))
WORKERS = int(os.getenv("WORKERS", 8))
TIMEOUT_KEEP_ALIVE = int(os.getenv("TIMEOUT_KEEP_ALIVE", 600))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
SECRET_KEY = os.getenv("SECRET_KEY")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

# API SETTINGS
DOMAIN = os.getenv("DOMAIN", "127.0.0.1")
DEBUG = str(os.getenv("DEBUG")).lower() == "true"
RELOAD = str(os.getenv("RELOAD")).lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
HOSTS = json.loads(os.getenv("HOSTS", '["127.0.0.1", "api-resights"]'))
ORIGINS = json.loads(os.getenv("ORIGINS", '["http://127.0.0.1:3000", "http://localhost:3000"]'))

# DB Settings
DATABASE_NAME = os.getenv("DATABASE_NAME", "printer24")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "root")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# Mail Settings
MAIL_API_KEY = os.getenv('KEY')
MAIL_SECRET_KEY = os.getenv('SECRET')
HOST_EMAIL = os.getenv('FROM')
