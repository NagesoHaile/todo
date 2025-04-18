from sqlmodel import Session,select
from app.models.task import Task
from typing import List,Optional

def create_taks(db:Session,task:Task)-> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db:Session,task_id:int)-> Optional[Task]:
    return db.get(Task,task_id)

def get_all_tasks(db:Session)->List[Task]:
    return db.exec(select(Task)).all()

"""
It takes [session] and task of Type Task
and returns Task
"""
def update_task(db:Session,task:Task)->Task:
    db.add(task)  # in this one SQLModel can track changes
    db.commit()
    db.refresh(task)
    return task

"""
function to delete a task with given [task_id]
and it returns boolean value based on the
database operations result.
"""
def delete_task(db:Session,task_id:int)->bool:
    task = db.get(Task,task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
