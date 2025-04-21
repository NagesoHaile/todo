from fastapi import APIRouter,Depends,Request
from app.schemas.user import UserRead
from app.models.user import User
from sqlmodel import Session
from app.config.database import get_session
from app.middleware.auth import JWTBearer
from app.services.user_services import get_profile

router = APIRouter(prefix='/user',tags=['Profile'],dependencies=[Depends(JWTBearer())])

@router.get('/profile')
def get_user_profile(request:Request,db:Session = Depends(get_session)):
    user_id = request.state.user.id
    print(f"user id : ---------> {user_id}")
    return get_profile(db=db,user_id=user_id)