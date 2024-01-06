from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from . import tables,schemas,functions

router=APIRouter()#Import environment variables from .env which was defined in docker-compose-pipe.yml

@router.post("/post_user",response_model=schemas.User_response_model)#Function receives JSON corresponding to "User_model"
async def adduser(data: schemas.User_model , db: Session=Depends(get_db)):
    data.password= functions.hash_fun(data.password)#Hash password (since storing the password in the original view is unsafe)
    new_user= tables.User_table(username=data.username,password=data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user#Return the same user row but without a password according to User_response_model.