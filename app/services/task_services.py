from sqlmodel import Session,select
from app.models.task import Task
from typing import List,Optional
from fastapi import HTTPException
from app.schemas.task import TaskRead
from app.schemas.response import SuccessResponse

def create_task(db:Session,task:Task)-> Task:
    """
        It takes db:Session and
        task:Task
        returns Task
    """
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db:Session,task_id:int)-> SuccessResponse:
    """
    Fetch a task by ID, wrap it in SuccessResponse.
    """
    try:
        task = db.exec(select(Task).where(Task.id == int(task_id)))
        if task is None:
            raise HTTPException(status_code=404,detail="Task not found")
        return SuccessResponse(data=task)
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error")




def get_all_tasks(db:Session):
    return db.exec(select(Task)).all()


def update_task(db:Session,task:Task)->Task:
    """
It takes [session] and task of Type Task
and returns Task
"""
    db.add(task)  # in this one SQLModel can track changes
    db.commit()
    db.refresh(task)
    return task


def delete_task(db:Session,task_id:int)->bool:
    """
function to delete a task with given [task_id]
and it returns boolean value based on the
database operations result.
"""
    task = db.get(Task,task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
