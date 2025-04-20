from fastapi import HTTPException,Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.utils.auth import decode_token
from app.models.user import User
from sqlmodel import Session
from app.config.database import get_session


class JWTBearer(HTTPBearer):
    def __init__(self,auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=401,detail="Authorization token missing"
            )
        session: Session = next(get_session())

        try:
            user = decode_token(credentials.credentials,session)
        except Exception:
            raise HTTPException(
                status_code=401,detail="Invalid token or token has expired"
            )
        request.state.user = user