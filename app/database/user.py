from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: str
    password: str
    username: str = Field(default=None)
    phone_number: str = Field(default=None)
    is_manager: bool = Field(default=None)
    points: int = Field(default=None)

class Payment(BaseModel):
    user_id: str
    amount: int
    token: str
