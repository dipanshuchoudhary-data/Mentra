from fastapi import Depends,Request
from backend.api.auth import get_current_user
from backend.utils.rate_limiter import rate_limit

def guarded(request:Request,user_id:str=Depends(get_current_user)):
    rate_limit(request,user_id)
    return user_id
