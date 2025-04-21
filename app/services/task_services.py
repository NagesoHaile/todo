from sqlmodel import Session,select
from app.models.task import Task
from typing import List,Optional
from fastapi import HTTPException
from app.schemas.task import TaskRead,TaskUpdate
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




def get_all_tasks(db:Session,is_completed:bool = None):
    command = select(Task)
    if is_completed is not None:
        return db.exec(command.where(Task.is_completed == is_completed)).all()
    return db.exec(command).all()


def update_task(db:Session,task_id:int,updates:TaskUpdate)->Task:
    """
It takes [session] and task of Type Task
and returns Task
"""
    try:
        task = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise HTTPException(status_code=404,detail="Task not found.")
        update_data = updates.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(task,key,value)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error")


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
