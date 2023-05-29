from fastapi import FastAPI
from app.routers import point, reservation, stadium, user

app = FastAPI()

app.include_router(point.router)
app.include_router(reservation.router)
app.include_router(stadium.router)
app.include_router(user.router)