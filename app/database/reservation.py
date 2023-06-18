from pydantic import BaseModel, Field
from typing import List
#from datetime import datetime

class Reservation(BaseModel):
    user_id : str
    stadium_id : str
    date : str
    time : List[str]
    is_paid : bool = False