from fastapi import FastAPI, HTTPException, status
from typing import List

from app.models.rooms import RoomResponse, RoomCreate, RoomDB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.base_db import get_session

app = FastAPI(
    title="RS Residency API",
    description="API for RS Residency",
    version="0.0.1"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to RS Residency!"} 

@app.get("/rooms", response_model=List[RoomResponse], 
         summary="Get all rooms",
         description="Retrieve a list of all available rooms")
def get_rooms():
    try:
        with get_session() as session:
            rooms = RoomDB.get_all_rooms(session)
            return rooms
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve rooms"
        )

@app.post("/rooms", 
          response_model=RoomResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Create a new room",
          description="Create a new room with the provided details")
def create_room(room: RoomCreate):
    try:
        with get_session() as session:
            db_room = RoomDB(
                name=room.name,
                room_type=room.room_type,
                floor=room.floor,
                capacity=room.capacity,
                price_per_night=room.price_per_night,
                amenities=room.amenities
            )
            session.add(db_room)
            session.commit()
            session.refresh(db_room)
            return db_room
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create room"
        )



