from fastapi import APIRouter,HTTPException,Depends,Header
import firebase_admin
from firebase_admin import auth,credentials

router = APIRouter()

if not firebase_admin._apps:
    firebase_admin.initialize_app()

def get_current_user(authorization:str=Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    try:
        decoded = auth.verify_id_token(token)
        return decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
@router.get("/me")
def me(user_id:str= Depends(get_current_user)):
    return {"user_id":user_id}