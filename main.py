from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

from bson import ObjectId
from fastapi.responses import JSONResponse

app = FastAPI()

# MongoDB 연결 설정
client = MongoClient("mongodb+srv://1820:capstone1820@sporting-capstone.fg3joe2.mongodb.net/")
db = client["mydatabase"]
collection = db["users"]

class User(BaseModel):
    name: str
    email: str

# 사용자 생성
@app.post("/users")
def create_user(user: User):
    user_data = user.dict()
    inserted_user = collection.insert_one(user_data)
    return {"message": "User created successfully", "user_id": str(inserted_user.inserted_id)}

# 사용자 조회
@app.get("/users/{user_id}")
def read_user(user_id: str):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])  # ObjectId를 문자열로 변환
        return user
    return {"message": "User not found"}

#모든 사용자 조회
@app.get("/users")
def get_all_users():
    users = collection.find()
    users = list(users)
    for user in users:
        user["_id"] = str(user["_id"])  # ObjectId를 문자열로 변환
    return JSONResponse(content=users)

# 사용자 수정
@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: dict):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
        if result.modified_count > 0:
            return {"message": "User updated successfully"}
        else:
            return {"message": "Failed to update user"}
    else:
        return {"message": "User not found"}

# 사용자 삭제
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count > 0:
            return {"message": "User deleted successfully"}
        else:
            return {"message": "Failed to delete user"}
    else:
        return {"message": "User not found"}
