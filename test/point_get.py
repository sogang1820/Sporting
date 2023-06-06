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

params = {
    "user_id": "cstrnull00"
}

# POST 요청 보내기
response = requests.post(SERVICE_URL + f"points/{params['user_id']}")

# 응답 확인
if response.status_code == 201:
    response_data = response.json()
    print(response_data)
else:
    print(response.text)
