from sqlalchemy import Column, Integer, String
from authlogin.src.__init__ import Base


# Make class for users model
# Make new or use table in database
class Users(Base):
    __tablename__ = "users_auth"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    username = Column(String(30), unique=True)
    password = Column(String(255))

    def __repr__(self) -> str:
        return f"user:{self.name}, {self.username}"
