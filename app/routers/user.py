from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

from app.database import user_collection
from app.database.user import User
from app.services.login import login_user

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", status_code=201)
def signup(user:User):
    # signup
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    result = user_collection.insert_one(user_dict)
    user_id = str(result.inserted_id)

    return JSONResponse(content={"message": "User Created", "user_id": user_id}, status_code=201)

@router.post("/login")
def login(user: User):
    #login
    access_token = login_user(user.user_id, user.password)
    if access_token:
        return JSONResponse(content={"message": "Login successful", "access_token": access_token})
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
@router.post("/logout")
def logout():
    # logout
    return JSONResponse(content={"message": "Logout successful"})