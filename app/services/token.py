import jwt
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def verify_token(token, user_id):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expiration_time = decoded_token.get('exp')
        if expiration_time is None or datetime.utcnow() > datetime.fromtimestamp(expiration_time) or user_id != decoded_token.get("user_id"):
            return False
        return True
    except jwt.InvalidTokenError:
        return False