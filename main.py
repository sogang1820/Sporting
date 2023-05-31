from fastapi import FastAPI
from app.routers import point, reservation, stadium, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(point.router)
app.include_router(reservation.router)
app.include_router(stadium.router)
app.include_router(user.router)