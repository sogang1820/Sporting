from pydantic import BaseModel, Field

from app.database.user import User
from app.database.stadium import Stadium

class Reservation(BaseModel):
    user_id : str
    stadium_id : str 
    date : int
    time : int