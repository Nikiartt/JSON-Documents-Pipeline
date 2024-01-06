from fastapi import FastAPI,Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from datetime import datetime
from kafka import KafkaProducer
from . import tables,schemas,users,Authentication
from .database import engine


tables.Base.metadata.create_all(bind=engine)#Create the table "users" in it doesn't exist.

app =FastAPI()
app.include_router(Authentication.router)#Share FastAPI to "Authentication" and "users" files.(after we use "@router" instead of "@app")
app.include_router(users.router)

#This link was created for debugging (we can check the API proper work remotely)
@app.get("/")
async def root():
    return {"message": "Hello World"}
#The main function of code, which refers to InvoiceItem that is inherited from the base model 
@app.post("/document")
async def post_invoice_item(item: schemas.InvoiceItem,user_id:int=Depends(Authentication.get_current_user)):#Function accepts json document and token, which will be tested for for expire time and reliability. 
    try:#The try block prevents a entire crash of the server
        datetime_str = str(item.InvoiceDate)# Here is the part that converts received JSON Invoicedate values to proper format since we do have not-standard format in CSV
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
        item.InvoiceDate = datetime_object.strftime("%d-%m-%Y %H:%M:%S")# We rewrite the converted value back to JSON
        json_of_item = jsonable_encoder(item)
        json_as_string = json.dumps(json_of_item)#we convert back to JSON string the dictionary since Kafka reads binary JSON string in the producer port
        produce_kafka_string(json_as_string)
        return JSONResponse(content=json_of_item, status_code=201)
    except ValueError: # In the exception  we receive to user the provided JSON and print the error in the console
        return JSONResponse(content=jsonable_encoder(item), status_code=400)
# The Kafka producer function which sends to the producer in the inner docker port the JSON string
def produce_kafka_string(json_as_string):
    producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)
    producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
    producer.flush() 


