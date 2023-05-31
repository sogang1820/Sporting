from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.database import user_collection
from app.database.user import User
from app.services.login import login_user
from app.services.token import verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.options("/login")
async def options_logion():
    return {"Allow": "POST, OPTIONS"}

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

@router.get("/users/{user_id}/profile")
def get_user(user_id: str, token: str = Depends(oauth2_scheme)):
    # Access token verify
    if not verify_token(token, user_id):
        raise HTTPException(status_code=401, detail="Invalid access token")

    # Find User info
    user = user_collection.find_one({"user_id": user_id}, projection={"_id": False})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")