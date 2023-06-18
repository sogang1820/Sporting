import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")

def get_stadiums(page: int, per_page: int):
    url = SERVICE_URL + "stadiums"

    params = {
        "page": page,
        "per_page": per_page
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        total_count = data.get("total_count")
        page = data.get("page")
        per_page = data.get("per_page")
        stadiums = data.get("stadiums")

        # 결과 처리
        print(f"Total Count: {total_count}")
        print(f"Page: {page}")
        print(f"Per Page: {per_page}")
        print("Stadiums:")
        for stadium in stadiums:
            stadium["_id"] = str(stadium["_id"])
            print(json.dumps(stadium, indent=2))
    else:
        print("Failed to get stadiums.")

# 예시 사용
page = 1
per_page = 10

get_stadiums(page, per_page)