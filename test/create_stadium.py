import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

endpoint = "stadiums"  # 엔드포인트

# 요청 데이터
stadium_data = {
    "stadium_name": "Gwangju KIA Champions Field",
    "stadium_location": "Gwangju",
    "stadium_price": 100,
    "sports_category": "Baseball",
    "stadium_img": base64.b64encode(b"example image").decode("utf-8"),  # 이미지 데이터를 Base64로 인코딩하여 문자열로 변환
    "operating_hours": "Example Hours",
    "stadium_info": "Home stadium of KIA Tigers"
}

headers = {
    "Content-Type": "application/json",
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMSIsImV4cCI6MTY4NjEzNjE1M30.Oyz3RI5Lx-jKtGSuv6djVf0PBLJOuUzj3hr8h4AhA1c"
}

url = SERVICE_URL + endpoint

response = requests.post(url, data=json.dumps(stadium_data), headers=headers)

if response.status_code == 201:
    print("Stadium created successfully.")
else:
    print("Failed to create stadium.")
