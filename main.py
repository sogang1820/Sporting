from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
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
    user = collection.find_one({"_id": user_id})
    if user:
        return user
    return {"message": "User not found"}


# 사용자 수정
@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: User):
    user_data = updated_user.dict()
    updated_user = collection.update_one({"_id": user_id}, {"$set": user_data})
    if updated_user.modified_count > 0:
        return {"message": "User updated successfully"}
    return {"message": "User not found"}


# 사용자 삭제
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    deleted_user = collection.delete_one({"_id": user_id})
    if deleted_user.deleted_count > 0:
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}
