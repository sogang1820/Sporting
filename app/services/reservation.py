from app.database import reservation_collection

def get_stadium_reservations(stadium_id: str):
    stadium_reservations = reservation_collection.find({"stadium_id": stadium_id})
    reservations = [reservation for reservation in stadium_reservations]
    return reservations
