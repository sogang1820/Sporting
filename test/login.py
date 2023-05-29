import requests
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

# 로그인에 사용할 사용자 정보
user_info = {
    "user_id": "cstrnull00",
    "password": "20181600"
}

# POST 요청 보내기
response = requests.post(SERVICE_URL+"login", json=user_info)

# 응답 확인
if response.status_code == 200:
    print("로그인 성공")
else:
    print("로그인 실패:", response.text)
