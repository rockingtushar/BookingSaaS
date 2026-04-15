from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))

    business = relationship("Business", back_populates="services")