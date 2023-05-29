from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import PyJWTError
from app.database import user_collection
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id):
    expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + expires_delta
    encoded_jwt = jwt.encode({"user_id": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_user(user_id: str, password: str):
    user = user_collection.find_one({"user_id": user_id})
    if user and verify_password(password, user["password"]):
        access_token = create_access_token(user["user_id"])
        return access_token
    else:
        return None