from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
import uuid
from pydantic import BaseModel, EmailStr
from dbconfig import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class UserReqModel(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        form_attributes = True


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    complete = Column(Boolean, default=False)
    owner_id = Column(String)
    
class TodoReqModel(BaseModel):
    title: str
    description: str
    complete: bool = False
    owner_id: str

    class Config:
        form_attributes = True