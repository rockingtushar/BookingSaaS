from pydantic import BaseModel
from typing import Optional

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    duration_minutes: Optional[int] = None