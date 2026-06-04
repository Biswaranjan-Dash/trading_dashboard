from sqlalchemy import Column, String, Integer
from app.core.database import Base

class User(Base):
    __tablename__="users"
    user_name = Column(String(100), primary_key=True)
    hashed_password = Column(String(255))
    balance = Column(Integer(), default=1000)
