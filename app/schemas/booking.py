from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    customer_id: int
    service_id: int
    date: datetime