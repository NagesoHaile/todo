import os
from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError,jwt
from sqlmodel import Session
from dotenv import load_dotenv
from app.schemas.user import TokenData
from fastapi import Depends,HTTPException,status
from app.config.database import get_session
from app.models.user import User


load_dotenv()
JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 30
def create_access_token(data:dict,expires_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=30))
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY,algorithm=ALGORITHM)


def decode_token(token: str, session: Session) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = session.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

# def decode_token(token:str,session:Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate':"Bearer"}
    )
  
    print(f"secret key {JWT_SECRET_KEY}")
    try:
        payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception

    print("payload")
    user_id = payload.get('sub')
    print(f"user id {user_id}")
    if user_id is None:
        raise credentials_exception
    token_data = TokenData(user_id=user_id)
    print(f"token data {token_data}")
    
    # user = session.get(User,token_data.user_id)

    # if user_id is None:
    #     raise credentials_exception
    return token_data