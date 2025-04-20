from typing import Optional,List
from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

# for creating tasks

class TaskCreate(TaskBase):
    """
 Schema used for creating a task
 
"""
    user_id:Optional[int] = None 


class TaskRead(TaskBase):
    """
        schema used to read a task
        DB -> client
    """
    id: int
    user_id: Optional[int]


    class Config:
        orm_mode = True


class TaskListResponse(BaseModel):
    ok:bool = True
    data:List[TaskRead] = None