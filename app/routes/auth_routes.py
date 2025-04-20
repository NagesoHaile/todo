from fastapi import APIRouter,Depends
from app.schemas.response import SuccessResponse,ErrorResponse
from app.services.auth_services import register_user,login_user,reset_user_password
from app.schemas.user import UserCreate,UserLogin,ResetPassword
from sqlmodel import Session
from app.config.database import get_session

router = APIRouter()

@router.post("/register",response_model=SuccessResponse)
def register(data:UserCreate,session:Session = Depends(get_session)):
    return register_user(data=data,db=session)

@router.post("/login",response_model=SuccessResponse)
def login(data:UserLogin,session:Session = Depends(get_session)):
    return login_user(data=data,db=session)


@router.post("/reset-password",response_model=SuccessResponse)
def reset_password(data:ResetPassword,session:Session = Depends(get_session)):
    return reset_user_password(data=data,db=session)
