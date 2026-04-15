from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    phone: str