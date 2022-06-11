from unicodedata import name
from sqlalchemy.orm import Session
from authlogin.src.schemas.users import *
from authlogin.src.model.users import Users
from bcrypt import hashpw, gensalt


class HandUser:
    async def create_user(db: Session, item: CreateUser):
        pw = item.password.encode("utf-8")
        hashed = hashpw(pw, gensalt())
        user = Users(name=item.name, username=item.username, password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def by_username(db: Session, _username):
        user = db.query(Users).filter(Users.username == _username).first()
        return user

    def get_user(db: Session, _username, _password):
        user = db.query(User).filter(Users.username == _username, Users.password == _password)
        return user

    def delete_user(db: Session, _username):
        user = db.query(Users).filter(Users.username == _username).first()
        db.delete(user)
        db.commit()
        return {"msg": "user berhasil terhapus"}

    def update_user(db: Session, item: CreateUser):
        user = db.merge(item)
        db.commit()
        db.refresh(user)
        return user
