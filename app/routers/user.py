from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import collection

router = APIRouter()

@router.get("/users")
def get_users():
    users = collection.find()
    users = list(users)
    for user in users:
        user["_id"] = str(user["_id"])  # ObjectId를 문자열로 변환
    return JSONResponse(content=users)
