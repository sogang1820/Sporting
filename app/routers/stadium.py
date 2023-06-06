from fastapi import APIRouter, HTTPException, responses, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from app.database import stadium_collection
from app.database.stadium import Stadium
from app.database.user import User

from app.services.token import get_current_user

router = APIRouter()

@router.post("/stadiums", status_code=201)
def create_stadium(stadium: Stadium, current_user: User = Depends(get_current_user)):

    if not current_user.is_manager:
        raise HTTPException(status_code=401, detail="Unauthorized")

    is_exist = stadium_collection.find_one({
        "stadium_name": stadium.stadium_name,
        "stadium_location": stadium.stadium_location,
        "sports_category": stadium.sports_category
    })

    if is_exist:
        raise HTTPException(status_code=400, detail="Stadium already exists")

    stadium_collection.insert_one(stadium.dict())

    return JSONResponse(content={"message": "Stadium Created"}, status_code=201)

@router.get("/stadiums/{stadium_id}")
def read_stadium(stadium_id: str):
    stadium = stadium_collection.find_one({"_id": ObjectId(stadium_id)})

    if stadium:
        stadium.pop("_id")        

        #TODO
        #구장에 관련된 예약 항목 보여주기

        return stadium
    else:
        raise HTTPException(status_code=404, detail="Stadium not found")
    
@router.put("/stadiums/{stadium_id}")
def update_stadium(stadium_id: str, updated_stadium: Stadium, current_user: User = Depends(get_current_user)):

    if not current_user.is_manager:
        raise HTTPException(status_code=401, detail="Unauthorized")

    stadium = stadium_collection.find_one({"stadium_id": stadium_id})
    if stadium:
        update_result = stadium_collection.update_one({"stadium_id": stadium_id}, {"$set": updated_stadium.dict()})

        if update_result.modified_count > 0:
            return JSONResponse(content={"message": "Stadium updated successfully"})
        else:
            raise HTTPException(status_code=500, detail="Failed to update")
    else:
        raise HTTPException(status_code=401, detail="Stadium Not Found")
    
@router.delete("/stadiums/{stadium_id}")
def delete_stadium(stadium_id: str, current_user: User = Depends(get_current_user)):

    if not current_user.is_manager:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = stadium_collection.delete_one({"_id": ObjectId(stadium_id)})
    if result.deleted_count == 1:
        return responses.Response(status_code=204)
    else:
        raise HTTPException(status_code=500, detail="Failed to delete stadium")