import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")
endpoint = "reservations"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY3N0cm51bGwwMCIsImV4cCI6MTY4NzA1NzA4MX0.d8EJ_Xaoep59EoJauPs4pgNrCeax4alzeAXNqYvbdMA"
}
reservation_data = {
    "user_id": "cstrnull00",
    "stadium_id": "648d41d468fb7e7d7fb6c838",
    "date": "2023-06-19",
    "time": ["10:00", "12:00"]
}

url = SERVICE_URL + endpoint

# POST 요청 보내기
response = requests.post(url, json=reservation_data, headers=headers)

# 응답 확인
if response.status_code == 201:
    print("Reservation created successfully.")
else:
    print(response.text)
