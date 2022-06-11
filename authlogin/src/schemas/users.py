from typing import Optional
from pydantic import BaseModel
from fastapi import Form


# make base for pydantic schemass
class UserBase(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    # schemas for allowed request form in template
    @classmethod
    def register(cls, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
        return cls(name=name, username=username, password=password)

    # schemas for allowed request form in template
    @classmethod
    def login(cls, username: str = Form(...), password: str = Form(...)):
        return cls(username=username, password=password)


class CreateUser(UserBase):
    pass


class User(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True
