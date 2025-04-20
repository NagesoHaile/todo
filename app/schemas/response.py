from pydantic import BaseModel
from typing import Any,Dict,Optional


class SuccessResponse(BaseModel):
    ok:bool =True
    data:Any


class ErrorResponse(BaseModel):
    ok: bool = False
    message:str
    details: Optional[Dict[str,Any]] = None