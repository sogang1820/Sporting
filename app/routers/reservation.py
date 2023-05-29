from fastapi import APIRouter

router = APIRouter()

@router.get("/reservations")
def get_points():
    return {"message": "This is the reservations endpoint"}
