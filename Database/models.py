from sqlalchemy import Column, String, Integer, ForeignKey
from Database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)