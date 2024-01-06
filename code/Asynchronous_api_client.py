import aiohttp
import asyncio
import pandas as pd
from json import loads
import time
import requests 

#Parameters
post_numbers=2000 #Choose how many rows you want to upload from upload.csv file
attempts=0 #Each request with response status not 201 will be resented 
url='http://127.0.0.1:80/document'
token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDQ1NDYxMDl9.5OX3iDsufK38oDJa21hcNQGFFa0ToGHuJXXuEFUE_9w"

#Preparation of data for aiohttp (use the main directory)
df_all=pd.read_csv('../data/upload.csv') #Read and store as pandas data frame all data from upload.csv
df_cuted=df_all.iloc[0:post_numbers] 
print('df_cuted prepared')
str = df_cuted.to_json(orient="records") #Extract data from pandas data frame as string
print('str prepared')
dict = loads(str) #Transform string into dictionary since we will use it in requests and aiohttp 
print('dict prepared')

errors_postNumbers=[]#This list will store all post numbers that will have status-code, not 201 (we will send these posts a second time using request)
Not_Passed=[] #List will store all the post numbers that did not pass through asynchronous and simple request functions

#The second asynchronous function will be received from the first function session and post number.
#The function will sort all 201 responses and will repeat those that had incorrect status code.
#All not passed JSON documents will be stored in a list as a post numbers.
async def get_page_page(session , post_number):
  try:
    repeat=0
    while True:
      repeat=repeat+1
      response=await session.post(url=url,headers={'Authorization': f'Bearer {token}'}, json=dict[post_number])
      if response.status==201:
        print("PASSED","post_number",post_number,"status",response.status,"LASTrepeat",repeat)
        break
      elif repeat>=attempts:
        print("TO MUCH ATTEMPTS","post_number",post_number,"LASTstatus",response.status,"LAST attempt",repeat)
        errors_postNumbers.append(post_number)
        break
      else:
        print("REPEAT","post_number",post_number,"status",response.status,"attempts",repeat)
  except Exception as e:
    print(f"ERROR IN POST NUMBER{post_number}\n",e)
    errors_postNumbers.append(post_number)

# The first function will create a tasks for even loop as well as session
async def asynchronous():
  async with aiohttp.ClientSession() as session:
    tasks=[]
    for post_number in range(post_numbers):
        task= asyncio.create_task(get_page_page(session , post_number))
        tasks.append(task)
    print('Tasks prepared')
    await asyncio.gather(*tasks)

# This function will try to resend all not passed rows using request library
def Requests(errors_postNumbers):
    for i in errors_postNumbers:
      response = requests.post(url, json=dict[i])
      print("Final attempt","post_number",i,"status",response.status_code)
      if response.status_code==201:
        pass
      else:
        Not_Passed.append(i)
# Condition allows to run code only when user runs code on his own computer (we can't run this code remotely).
if __name__=="__main__":
  start_time=time.time()
  asyncio.run(asynchronous())
  a_time=time.time()-start_time
  Requests(errors_postNumbers)
  r_time=time.time()-start_time
  speed=post_numbers/a_time

print('-----------Review-----------')
print('Posts',post_numbers)
print('Attempts to repeat',attempts)
print('Time of asynchronous function',round(a_time,3),'s')
print('Time of requests function',round(r_time,3),'s')
print('Average speed of accepting the requests',speed)
print("Number of not passed JSON documents after asynchronous function",len(errors_postNumbers))
print("Number of not passed JSON documents after requests function",len(Not_Passed))
