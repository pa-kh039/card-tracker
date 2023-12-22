from pydantic import BaseModel,Field
from datetime import datetime

class CardBase(BaseModel):
    id: str
    status: str

class CardFull(CardBase):
    user_phone: str= Field(pattern=r'^\+?[1-9]\d{1,14}$')

class UserBase(BaseModel):
    phone_num: str= Field(pattern=r'^\+?[1-9]\d{1,14}$')
    name: str
