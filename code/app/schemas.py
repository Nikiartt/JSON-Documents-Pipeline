from pydantic import BaseModel
from datetime import datetime
from typing import Optional
#The main storage of schemas that defines inputs, outputs and other data transactions in the code.
class User_model(BaseModel):
    username:str
    password:str
    class Config:
        orm_mode = True

class User_response_model(BaseModel):
    id:int
    username:str
    created_at:datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None

class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str 
    Description: str 
    Quantity: int 
    InvoiceDate: str 
    UnitPrice: float 
    CustomerID: int 
    Country: str 