from typing import Optional,List
from sqlmodel import SQLModel,Field,Relationship


class Task(SQLModel,table=True):
    __tablename__ = 'tasks'

    id: Optional[int] = Field(default=None,primary_key=True)
    title:str
    description:Optional[str] = None
    is_completed: bool = Field(default=False)

    user_id: int = Field(foreign_key = 'users.id')

    owner: Optional["User"] = Relationship(back_populates = 'tasks')
