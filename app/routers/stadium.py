from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import stadium_collection

router = APIRouter()

@router.get("/stadiums")
def get_points():
    return {"message": "This is the stadiums endpoint"}
