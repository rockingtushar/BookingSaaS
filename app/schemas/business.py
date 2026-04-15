from pydantic import BaseModel

class BusinessCreate(BaseModel):
    name: str
    email: str
    password: str
    type: str

class BusinessLogin(BaseModel):
    email: str
    password: str

class BusinessOut(BaseModel):
    id: int
    name: str
    email: str
    type: str

    class Config:
        from_attributes = True