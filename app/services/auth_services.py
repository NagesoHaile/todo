from app.models.user import User
from app.utils.password import hash_password,verify_password
from app.utils.auth import create_access_token,decode_token

from app.config.database import get_session
from sqlmodel import Session,select
from fastapi import HTTPException,Depends
from app.schemas.response import SuccessResponse,ErrorResponse
from app.schemas.user import UserCreate,UserRead,UserLogin



def register_user(data:UserCreate,db:Session):
    # check if user already exists
    existing_user = db.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )
    hashed_password = hash_password(data.password)

    new_user = User(name=data.name,email=data.email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = UserRead(id=new_user.id,email=new_user.email,name=new_user.name)
    return SuccessResponse(ok=True,data=response)
    

def login_user(data:UserLogin,db:Session):
    user = db.exec(select(User).where(User.email == data.email)).first()
    print("login.............. ")
    print(user)
    if not user or  not verify_password(data.password,user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalide credentials.",
        )
    
    token = create_access_token({"sub":str(user.id)})

    return SuccessResponse(ok=True,data={"access_token":token})


def reset_user_password(email:str,new_password:str, db:Session):
    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            response_model = ErrorResponse
        )
    
    hashed_password = hash_password(new_password)
    user.hashed_password = hashed_password
    # db.add(user)
    db.commit()
    return SuccessResponse(ok=True,data={"message:":"Password successfully reset"})