from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime , timedelta
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import tables,schemas,functions
from .config import Settings

settings=Settings()#Import environment variables from .env which was defined in docker-compose-pipe.yml

router=APIRouter()#Receive the router class

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):#Function checks token for the ability to decode by the provided algorithm and the secret_key.
    try:
        payload=jwt.decode(token, key=settings.secret_key, algorithms=[settings.algorithm])
        id:int=payload.get('user_id')#After function checks the token for id (ID must be stored in token)
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)#Checks the token data according to the TokenData class inherited from BaseModel
    except JWTError:
        raise credentials_exception
    return token_data#Return token data (in this case it is only ID, but we can store more info).
    
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')#Create an instance of the class with a URL parameter (it has to match with URL where we want to implement this class)
def get_current_user(token:str=Depends(oauth2_scheme)):#Function takes a token string, creates an instance of HTTPException, and provides everything to the "verify_access_token" function
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                                        detail='Invalid credentials',\
                                        headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token, credentials_exception)

@router.post("/token")#The function returns the token in the credentials that are valid in Postgres in the "users" table.
def log_in(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user_row=db.query(tables.User_table).filter(tables.User_table.username==user_credentials.username).first()#Search for a row in "users" by a unique username
    if not user_row:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,#Check if the username exists
                            detail="Invalid credentials(username)")
    if not functions.verify_pass(user_credentials.password,user_row.password):#Check if the provided password matches with hashed password in "users"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials(password)")
    access_token=create_access_token(data={"user_id":user_row.id})
    return{'access_token':access_token, 'token_type':'Bearer'}#Return token with stored ID in no exceptions were raised  
