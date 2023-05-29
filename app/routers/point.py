from fastapi import APIRouter

router = APIRouter()

@router.get("/points")
def get_points():
    #point 관련 로직 처리
    return {"message": "Points API"}