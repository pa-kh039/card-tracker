from fastapi import status,HTTPException,APIRouter
import schemas,utils
from database import conn,cursor

router=APIRouter(prefix="/users",tags=['Users'])

#for future implementation of users