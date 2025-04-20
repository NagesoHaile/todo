from fastapi import APIRouter,Depends,status,Request
from sqlmodel import Session,select
from typing import List
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskListResponse,TaskUpdate
from app.config.database import get_session
from app.middleware.auth import JWTBearer
import app.services.task_services as TaskService

router = APIRouter(prefix='/tasks',tags=['Tasks'],dependencies=[Depends(JWTBearer())])

@router.get('',response_model=TaskListResponse)
def get_tasks(db:Session = Depends(get_session)):
     tasks =  TaskService.get_all_tasks(db=db)
     return {"ok":True,"data":tasks}
    

@router.post('',response_model=TaskCreate,status_code=status.HTTP_201_CREATED)
def create_task(request:Request,task:TaskCreate,db:Session = Depends(get_session)):
    user_id = request.state.user.id
    task.user_id = user_id
    new_task = Task.model_validate(task)
    return TaskService.create_task(db=db,task=new_task)


@router.get('/{task_id}')
def get_task_by_id(task_id:int,db:Session = Depends(get_session)):
    task = TaskService.get_task_by_id(db=db,task_id=task_id)
    return task

@router.put('/{task_id}')
def update_task(task_id:int,task:TaskUpdate,db:Session = Depends(get_session)):
    return TaskService.update_task(db=db,updates=task,task_id=task_id)


@router.delete('/{task_id}')
def delete_task(task_id:int,db:Session = Depends(get_session)):
    return TaskService.delete_task(db=db,task_id=task_id)