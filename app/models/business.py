from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    type = Column(String)

    services = relationship("Service", back_populates="business")
    customers = relationship("Customer", back_populates="business")
    bookings = relationship("Booking", back_populates="business")