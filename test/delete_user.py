import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

# 회원 탈퇴 요청 예시
def delete_user(user_id):
    url = SERVICE_URL + f"users/{user_id}"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGhhY2s5OCIsImV4cCI6MTY4NTU5NTQyNH0.IEhB8oa8dwb-h1C2YjhiAswjmgKQXp4BZiUg7IcT_N8"
 # 액세스 토큰

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(url, headers=headers)

    #print(response.json())

# 예시 사용
user_id = 'thack98'  # 실제 사용자 ID

delete_user(user_id)
