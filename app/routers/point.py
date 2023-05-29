from fastapi import APIRouter
from app.database import collection

router = APIRouter()

@router.get("/points")
def get_points():
    points = collection.find()
    return {"points": points}
