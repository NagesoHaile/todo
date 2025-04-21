from app.schemas.user import UserRead,UserUpdate
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

def update_profile(db:Session,user_id:int,updates:UserUpdate):
    """
        update current user profile
    """
    try:
        print(f"dataaaaaaaa => {updates}")
        command = select(User).where(User.id == user_id)
        user = db.exec(command).first()
        if not user or None:
            raise HTTPException(status_code=404,detail="User not found")
        update_data = updates.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(user,key,value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error.")