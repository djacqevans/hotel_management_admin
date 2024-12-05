from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

Base = declarative_base()

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    proof_of_identity: str
    proof_image_url: Optional[str] = None
    proof_image_filename: Optional[str] = None

    class Config:
        from_attributes = True

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    proof_of_identity = Column(String(200), nullable=False)
    proof_image_url = Column(String(500), nullable=True)
    proof_image_filename = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    @property
    def proof_image_key(self):
        """Generate the storage key for the proof image"""
        if self.proof_image_filename:
            return f"customer_proofs/{self.id}/{self.proof_image_filename}"
        return None

    @classmethod
    def get_all_customers(cls, session):
        return session.query(cls).all()
    
