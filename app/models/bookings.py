from datetime import datetime, date, timedelta
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, field_validator
from app.models.enums import BookingStatus, PaymentStatus
from typing import List, Optional

Base = declarative_base()

class BookingDB(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    # Booking dates
    scheduled_check_in = Column(Date)    # Original planned check-in
    scheduled_check_out = Column(Date)   # Original planned check-out
    actual_check_in = Column(DateTime, nullable=True)    # Actual check-in time
    actual_check_out = Column(DateTime, nullable=True)   # Actual check-out time
    
    # Status tracking
    booking_status = Column(String, default=BookingStatus.PREBOOKED.value)
    payment_status = Column(String, default=PaymentStatus.PENDING.value)
    
    # Payment tracking
    total_amount = Column(Numeric(10, 2))
    amount_paid = Column(Numeric(10, 2), default=0)
    
    # Additional charges (for late check-out etc.)
    additional_charges = Column(Numeric(10, 2), default=0)
    notes = Column(String, nullable=True)
    
    booking_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    room = relationship("RoomDB", back_populates="bookings", foreign_keys=[room_id])
    customer = relationship("CustomerDB", back_populates="bookings", foreign_keys=[customer_id])

    

    @classmethod
    def is_room_occupied(cls, session, room_id: int, check_date: date = None) -> bool:
        """
        Check if room has any current occupants or bookings for a specific date
        Args:
            session: Database session
            room_id: ID of the room to check
            check_date: Optional specific date to check (defaults to today)
        """
        if check_date is None:
            check_date = date.today()
            
        return session.query(cls).filter(
            cls.room_id == room_id,
            cls.booking_status.in_([BookingStatus.CHECKED_IN.value, BookingStatus.CONFIRMED.value, BookingStatus.PREBOOKED.value ]),
            cls.scheduled_check_in <= check_date,
            cls.scheduled_check_out > check_date
        ).first() is not None

    @classmethod
    def get_all_bookings(cls, session):
        return session.query(cls).all()

class BookingCreate(BaseModel):
    room_id: int
    customer_id: int
    scheduled_check_in: date
    scheduled_check_out: date
    payment_status: PaymentStatus
    booking_status: BookingStatus
    total_amount: float
    amount_paid: float
    additional_charges: float
    notes: Optional[str]

    @field_validator('scheduled_check_in')
    @classmethod
    def check_in_date_validation(cls, v):
        if v < date.today():
            raise ValueError("Check-in date cannot be in the past")
        return v

    @field_validator('scheduled_check_out')
    @classmethod
    def check_out_date_validation(cls, v, info):
        check_in = info.data.get('scheduled_check_in')
        if check_in and v <= check_in:
            raise ValueError("Check-out date must be after check-in date")
        return v

    @field_validator('amount_paid')
    @classmethod
    def amount_paid_validation(cls, v, info):
        if v < 0:
            raise ValueError("Amount paid cannot be negative")
        if 'total_amount' in info.data and v > info.data['total_amount']:
            raise ValueError("Amount paid cannot exceed total amount")
        return v

    @field_validator('total_amount')
    @classmethod
    def total_amount_validation(cls, v):
        if v <= 0:
            raise ValueError("Total amount must be greater than zero")
        return v

class BookingResponse(BaseModel):
    id: int
    room_id: int
    customer_id: int
    scheduled_check_in: date
    scheduled_check_out: date
    actual_check_in: Optional[datetime]
    actual_check_out: Optional[datetime]
    booking_status: str
    payment_status: str
    total_amount: float
    amount_paid: float
    additional_charges: float
    notes: Optional[str]
    booking_date: datetime

    class Config:
        from_attributes = True 