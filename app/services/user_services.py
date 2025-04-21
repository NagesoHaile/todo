from app.schemas.user import UserRead
from app.models.user import User
from sqlmodel import Session,select

from fastapi import HTTPException

def get_profile(db:Session,user_id:int)->UserRead:
    """
        get current user profile
    """
    try:
        user = db.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        u = user.model_dump(exclude=["hashed_password"])
        return u
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error.")
    