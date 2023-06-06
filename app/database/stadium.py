from pydantic import BaseModel, Field

class Stadium(BaseModel):
    stadium_name : str
    stadium_location : str
    stadium_price : int
    sports_category : str
    stadium_img : bytes
    operating_hours : str
    stadium_info : str
    manager_id : str = Field(default=None)