from sqlalchemy import Column, Integer, String
from database import Base 

class Card(Base):
    __tablename__='cards'

    id=Column(String,primary_key=True,nullable=False)
    status=Column(String,server_default='generated',nullable=False)
    user_phone=Column(String,nullable=False,unique=True)
