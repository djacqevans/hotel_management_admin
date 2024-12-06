from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime

from app.models.rooms import RoomResponse, RoomCreate, RoomDB
from app.models.customer import CustomerResponse, CustomerCreate, CustomerDB
from app.models.bookings import BookingDB, BookingCreate, BookingResponse
from app.models.enums import BookingStatus
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

@app.post("/create-room", 
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create room"
        )
    

@app.get("/customers", 
         response_model=List[CustomerResponse],
         summary="Get all customers",
         description="Retrieve a list of all customers")
def get_customers():
    try:
        with get_session() as session:
            customers = CustomerDB.get_all_customers(session)
            return customers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customers"
        )


@app.post("/create-customer", 
          response_model=CustomerResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Create a new customer",
          description="Create a new customer with the provided details")
def create_customer(customer: CustomerCreate):
    try:
        with get_session() as session:
            db_customer = CustomerDB(
                **customer.model_dump()
            )
            session.add(db_customer)
            session.commit()
            session.refresh(db_customer)
            return db_customer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create customer"
        )
    

@app.get("/bookings", 
         response_model=List[BookingResponse],
         summary="Get all bookings",
         description="Retrieve a list of all bookings")
def get_bookings():
    try:
        with get_session() as session:
            bookings = BookingDB.get_all_bookings(session)
            return bookings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve bookings"
        )

@app.post("/create-booking", 
          response_model=BookingResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Create a new booking",
          description="Create a new booking with the provided details")
def create_booking(booking: BookingCreate):
    try:
        with get_session() as session:
            
            # Check room availability
            if BookingDB.is_room_occupied(session, booking.room_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Room is currently occupied"
                )
                
            # Create booking
            db_booking = BookingDB(
                **booking.model_dump()
            )
            session.add(db_booking)
            session.commit()
            return db_booking
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bookings/{booking_id}/check-in")
def check_in(booking_id: int):
    try:
        with get_session() as session:
            
            booking = session.query(BookingDB).filter(BookingDB.id == booking_id).first()
            
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")
            
            
            
            booking.actual_check_in = datetime.utcnow()
            booking.booking_status = BookingStatus.CHECKED_IN
            session.commit()
            
            return {"message": "Check-in successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bookings/{booking_id}/check-out")
def check_out(booking_id: int):
    try:
        with get_session() as session:
           
            booking = session.query(BookingDB).filter(BookingDB.id == booking_id).first()
            
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")
            
            current_time = datetime.utcnow()
            booking.actual_check_out = current_time
            
            # Calculate any additional charges
            
            
            booking.booking_status = BookingStatus.CHECKED_OUT
            session.commit()
            
            return {
                "message": "Check-out successful",
                "additional_charges": "vds"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    try:
        with get_session() as session:
            booking = session.query(BookingDB).filter(BookingDB.id == booking_id).first()
            
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")
            
            if booking.booking_status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
                raise HTTPException(
                    status_code=400, 
                    detail="Cannot cancel booking in current status"
                )
            
            booking.booking_status = BookingStatus.CANCELLED
            session.commit()
            
            return {"message": "Booking cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))