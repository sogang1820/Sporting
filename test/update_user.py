import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

# 사용자 정보 수정 요청 예시
def update_user(user_id, updated_info):
    url = SERVICE_URL + f"users/{user_id}/profile"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoic3BvcnRpbmciLCJleHAiOjE2ODU1OTMzMTF9.zGnAZLN8rt3hbzwfwKDovUotablp8NSc8APO4Y5xnVM" 

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.put(url, json=updated_info, headers=headers)

    print(response.json())

# 예시 사용
user_id = 'sporting'  # 실제 사용자 ID
updated_info = {
    "user_id": "sporting",
    "password": "sporting1820",
    "username": "서강이"
}

update_user(user_id, updated_info)

