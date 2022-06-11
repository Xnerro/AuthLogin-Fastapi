from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from json import dumps

# load all element from file .env
load_dotenv()

engine = create_engine(f"{getenv('ENGINE')}://{getenv('USER')}@{getenv('HOST')}:{getenv('PORT')}/{getenv('DB')}")

Base = declarative_base()

session = sessionmaker(autocommit=False, bind=engine)

# connect to sql engine
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# in production you can use Settings management
# from pydantic to get secret key from .env
class Setting(BaseModel):
    authjwt_secret_key: str = getenv("SECRET_KEY_JWT")


# add setting to AuthJW
@AuthJWT.load_config
def get_config():
    return Setting()
