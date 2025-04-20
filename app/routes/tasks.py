from fastapi import APIRouter,Depends, HTTPException,status
from sqlmodel import Session,select
from typing import List
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskRead
from app.config.database import get_session
from app.middleware.auth import JWTBearer

router = APIRouter(prefix='/tasks',tags=['Tasks'])

@router.get('',response_model=List[TaskRead],dependencies=[Depends(JWTBearer())])
def get_tasks(db:Session = Depends(get_session)):
    command = select(Task)
    tasks = db.exec(command).all()
    return tasks

@router.post('',response_model=TaskCreate,status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate,db:Session = Depends(get_session)):
    new_task = Task.model_validate(task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    