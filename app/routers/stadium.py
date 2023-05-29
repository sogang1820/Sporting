from fastapi import APIRouter

router = APIRouter()

@router.get("/stadiums")
def get_points():
    return {"message": "This is the stadiums endpoint"}
