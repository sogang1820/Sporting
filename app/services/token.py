from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from dotenv import load_dotenv
from datetime import datetime
import os

from app.database.user import User
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
    
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWTError):
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        user = user_collection.find_one({"user_id": user_id})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")