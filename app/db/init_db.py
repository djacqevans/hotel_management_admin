from app.models.base import Base
from app.db.base_db import engine

# Import all models here
from app.models.rooms import RoomDB
from app.models.bookings import BookingDB
from app.models.customer import CustomerDB

def init_db():
    Base.metadata.create_all(bind=engine)
