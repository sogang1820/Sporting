from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from dotenv import load_dotenv
from datetime import datetime
import os

from app.database import user_collection

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token, user_id):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expiration_time = decoded_token.get('exp')
        if expiration_time is None or datetime.utcnow() > datetime.fromtimestamp(expiration_time) or user_id != decoded_token.get("user_id"):
            return False
        return True
    except jwt.InvalidTokenError:
        return False
    

def get_current_user(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = user_collection.find_one({"user_id": user_id})
        return user
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid authentication token")