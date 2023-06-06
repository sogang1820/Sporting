import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

payment_info = {
    "user_id": "cstrnull00",
    "amount": 50,
    "token": "aa"
}

# POST 요청 보내기
response = requests.post(SERVICE_URL+"payment",json=payment_info)

print(response.text)
