from fastapi import APIRouter,Depends,Request
from app.schemas.user import UserRead,UserUpdate
from app.models.user import User
from sqlmodel import Session
from app.config.database import get_session
from app.middleware.auth import JWTBearer
from app.services.user_services import get_profile,update_profile

router = APIRouter(prefix='/user',tags=['Profile'],dependencies=[Depends(JWTBearer())])

@router.get('/profile')
def get_user_profile(request:Request,db:Session = Depends(get_session)):
    user_id = request.state.user.id
    result =  get_profile(db=db,user_id=user_id)
    return {"ok":True,"data":result}

@router.put('/profile')
def update_user_profile(request:Request,data:UserUpdate,db:Session = Depends(get_session),):
    user_id = request.state.user.id
    result =  update_profile(db=db,user_id=user_id,updates=data)
    user = result.model_dump(exclude=['hashed_password'])
    return {"ok":True,"message":"Profile updated successfully","data":user}

