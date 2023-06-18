from fastapi import APIRouter, Request, Response
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from typing import Optional
import requests
import stripe
from app.database import user_collection
from app.database.user import Payment



router = APIRouter()
'''
@router.get("/points")
def get_points():
    #point 관련 로직 처리
    return {"message": "Points API"}
'''

# Stripe API 키 설정
stripe.api_key = "your_stripe_api_key"

#client = MongoClient("mongodb://localhost:27017")
#db = client["your_mongodb_database"]
#collection = db["user_points"]

# 결제 요청 핸들러
@router.post("/payment")
#async def make_payment(user_id: str, amount: int, token: str):
async def make_payment(payment:Payment):
    try:
        pay = payment.dict()
        # 사용자 포인트 잔액 확인
        user = user_collection.find_one({"user_id": pay['user_id']})

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user_balance = user.get("points", 0)

        # 포인트로 결제 가능한지 확인
        if pay['amount'] > user_balance:
            raise HTTPException(status_code=400, detail="Insufficient points.")
        '''
        # Stripe 결제 생성
        payment = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            description="Payment for order"
        )
        '''
        # 결제 성공 시 포인트 차감
        user_collection.update_one({"user_id": pay['user_id']}, {"$inc": {"points": -pay['amount']}})

        user_collection.update_one({"user_id": pay['manager_id']}, {"$inc": {"points": +pay['amount']}})

        # 결제 성공 시 응답
        return {"status": "success", "message": "Payment succeeded!"}

    except stripe.error.CardError as e:
        # 결제 실패 시 예외 처리
        error_message = e.json_body.get('error').get('message')
        raise HTTPException(status_code=400, detail=error_message)

    except Exception as e:
        # 기타 예외 처리
        raise HTTPException(status_code=500, detail="Payment failed.")


# 포인트 잔액 조회 핸들러
@router.post("/points/{user_id}")
async def get_user_points(user_id: str):
    user = user_collection.find_one({"user_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"user_id": user_id, "points": user.get("points", 0)}



'''
@app.post("/charge")
def charge(amount: int):
    # 카카오페이 API 엔드포인트와 헤더 설정
    url = "https://kapi.kakao.com/v1/payment/ready"
    headers = {
        "Authorization": "KakaoAK ${SERVICE_APP_ADMIN_KEY}",
        "Content-Type": "Content-type: application/x-www-form-urlencoded;charset=utf-8"
    }

    # 충전 요청을 위한 데이터 생성
    data = {
        "cid":"TC0ONETIME",
        "partner_order_id":"",
        "partner_user_id":"",
        "item_name":"",
        "quantity":"",
        "total_amount":"",
        "tax_free_amount":"",
        "approval_url":"",
        "cancel_url":"",
        "fail_url":"",

        "amount": amount,
        # 필요한 다른 데이터 추가
    }

    # 카카오페이 충전 요청 보내기
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    # 카카오페이 API 응답 처리 및 결과 반환
    if response.status_code == 200 and result["code"] == 0:
        return {"message": "충전이 완료되었습니다."}
    else:
        return {"message": "충전 요청에 실패했습니다.", "error": result["msg"]}
    
'''        
'''
# 서버 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
'''