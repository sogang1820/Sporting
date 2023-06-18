import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

# 회원가입에 사용할 사용자 정보
user_info = {
    "user_id": "cstrnull00",
    "password": "20181600",
    "username": "Dohyeon KIM",
    "phone_number": "1234567890",
    "is_manager": False
}

# POST 요청 보내기
response = requests.post(SERVICE_URL+"signup", json=user_info)

# 응답 확인
if response.status_code == 201:
    print("회원가입 성공")
    response_data = response.json()
    print(response_data)
    user_id = response_data["user_id"]
    print("사용자 ID:", user_id)
else:
    print("회원가입 실패:", response.text)
