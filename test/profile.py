import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY3N0cm51bGwwMCIsImV4cCI6MTY4NzA3MzIyOH0.cbQCMl6FInJ7bz5Stm0A293nSWyn3IC-2h7fyNeDepI"
}
params = {
    "user_id": "cstrnull00"
}
response = requests.get(SERVICE_URL + f"users/{params['user_id']}/profile", headers=headers)

if response.status_code == 200:
    user_info = response.json()
    print(user_info)
else:
    print("사용자 정보 요청 실패:", response.text)
