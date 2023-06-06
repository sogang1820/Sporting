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
    "stadium_name": "Example Stadium",
    "stadium_location": "Example Location",
    "stadium_price": 100,
    "sports_category": "Example Category",
    "stadium_img": base64.b64encode(b"example image").decode("utf-8"),  # 이미지 데이터를 Base64로 인코딩하여 문자열로 변환
    "operating_hours": "Example Hours",
    "stadium_info": "Example Info"
}

headers = {
    "Content-Type": "application/json",
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMSIsImV4cCI6MTY4NjA1NzU2Nn0.z3v0jQv4yzT36bFbXSsfwBQ4nrtRyQfssTM12ef26Cs"

}

url = SERVICE_URL + endpoint

response = requests.post(url, data=json.dumps(stadium_data), headers=headers)

if response.status_code == 201:
    print("Stadium created successfully.")
else:
    print("Failed to create stadium.")
