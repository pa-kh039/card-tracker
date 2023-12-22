from fastapi import status,HTTPException,Response,APIRouter
import schemas
from typing import List
from database import conn,cursor
import utils

router=APIRouter(prefix="",tags=['Cards'])

@router.get("/get_card_status/{user_input}",status_code=status.HTTP_200_OK,response_model=schemas.CardBase)
def return_status(user_input: str):
    if utils.is_phone_num(user_input):
        cursor.execute('''SELECT * FROM cards WHERE user_phone=%s''',(user_input,))
        card=cursor.fetchone()
        if card==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No card linked with given phone no.")
        return card
    elif utils.is_card_id(user_input):
        cursor.execute('''SELECT * FROM cards WHERE id=%s''',(user_input,))
        card=cursor.fetchone()
        if card==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No card found with given id")
        return card
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="provided parameter is invalid")
