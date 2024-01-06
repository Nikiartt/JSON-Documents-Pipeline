
from pydantic_settings import BaseSettings ,SettingsConfigDict

class Settings(BaseSettings):#Class takes data from .env and returns it accordingly to scheme
    host:str
    userdb:str
    password:str
    database:str
    port:int
    secret_key:str
    access_token_expire_minutes:int
    algorithm:str
    model_config = SettingsConfigDict(env_file=".env")

