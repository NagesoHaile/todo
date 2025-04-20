from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title:str
    description: Optional[str] = None
    is_completed: bool = False

# for creating tasks
"""
 Schema used for creating a task
 
"""
class TaskCreate(TaskBase):
    pass 

"""
 schema used to read a task
 DB -> client
"""
class TaskRead(TaskBase):
    id: int
    created_at:datetime
    updated_at:datetime
    owner_id: Optional[int]


    class Config:
        orm_mode = True

