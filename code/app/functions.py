from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')#Define hash type 

def hash_fun(password):#Hashing function
    hashed_pass=pwd_context.hash(password)
    return  hashed_pass

def verify_pass(plain_pass,hashed_pass):#Function takes not hashed and hashed passwords and returns "True" boolean if they match
    return pwd_context.verify(plain_pass,hashed_pass)