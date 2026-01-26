from fastapi import Depends,Request
from api.auth import get_current_user
from utils.rate_limiter import rate_limit

def guarded(request:Request,user_id:str=Depends(get_current_user)):
    rate_limit(request,user_id)
    return user_id
