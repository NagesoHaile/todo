from typing import Optional,List
from sqlmodel import SQLModel,Field,Relationship
from .task import Task


class User(SQLModel,table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default = None,primary_key = True)
    name: str
    email = str = Field(index = True, unique = True)
    hashed_password: str

    tasks: List[Task] = Relationship(back_populates='owner')

