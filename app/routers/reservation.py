from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import reservation_collection

router = APIRouter()

@router.get("/reservations")
def get_points():
    return {"message": "This is the reservations endpoint"}
