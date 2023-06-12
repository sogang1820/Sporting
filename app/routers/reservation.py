from fastapi import APIRouter, HTTPException, responses, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from datetime import datetime

from app.database import reservation_collection
from app.database import stadium_collection

from app.database.reservation import Reservation

from app.services.token import get_current_user
from app.services.reservation import get_stadium_reservations

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/reservations", status_code=201)
async def make_reservation(reservation: Reservation, token: str = Depends(oauth2_scheme)):

    current_user = get_current_user(token)

    current_time = datetime.now().date()
    reservation_datetime = datetime.strptime(reservation.date, "%Y-%m-%d").date()

    if reservation_datetime < current_time:
        raise HTTPException(status_code=400, detail="Cannot make a reservation in the past")

    for time_slot in reservation.time:
        time_slot_datetime = datetime.strptime(time_slot, "%H:%M").time()
        if reservation.date == current_time.strftime("%Y-%m-%d") and time_slot_datetime <= current_time.time():
            raise HTTPException(status_code=400, detail="Cannot make a reservation in the past or present")

    is_exist = reservation_collection.find_one({
        "stadium_id": reservation.stadium_id,
        "date": reservation.date,
        "time": {"$in": reservation.time}
    })

    if is_exist:
        raise HTTPException(status_code=400, detail="Reservation already exists")

    reservation.user_id = current_user["user_id"]
    reservation_collection.insert_one(reservation.dict())

    return JSONResponse(content={"message": "Reservation Complete"})

@router.get("/admin/reservations")
def get_admin_reservations(token: str = Depends(oauth2_scheme)):

    current_user = get_current_user(token)

    if not current_user["is_manager"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    managed_stadiums = stadium_collection.find({"manager_id" : current_user["user_id"]})

    reservations = []

    for stadium in managed_stadiums:
        stadium_reservations = get_stadium_reservations(stadium["_id"])
        reservations.extend(stadium_reservations)

    return reservations

@router.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: str, token: str = Depends(oauth2_scheme)):

    current_user = get_current_user(token)
    reservation = reservation_collection.find_one({"reservation_id" : reservation_id})

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation Not Found")

    if reservation["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = reservation_collection.delete_one({"_id": ObjectId(reservation_id)})
    if result.deleted_count == 1:
        return responses.Response(status_code=204)
    else:
        raise HTTPException(status_code=500, detail="Failed to cancel reservation")