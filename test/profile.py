import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY3N0cm51bGwwMCIsImV4cCI6MTY4NTQ1NzYwMn0._wTAFHieY0evolyAvYgr5AQjeiEKYYV4L8y6sg2aq44"
}
params = {
    "user_id": "cstrnull00"
}
response = requests.get(SERVICE_URL + f"users/{params['user_id']}/profile", headers=headers)

if response.status_code == 200:
    user_info = response.json()
    print("사용자 정보:")
    print("이름:", user_info["user_id"])
    print("이메일:", user_info["username"])
    # 필요한 정보에 따라 추가적으로 처리
else:
    print("사용자 정보 요청 실패:", response.text)
