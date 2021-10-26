from sqlalchemy import Column, Integer, String 
from sqlalchemy.types import Date 
from .database import Base 


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    role = Column(String(20) )
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)