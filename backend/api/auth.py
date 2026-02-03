from fastapi import APIRouter, HTTPException, Depends, Header

import firebase_admin
from firebase_admin import auth

router = APIRouter()


# ---------------------------------------------------------
# Firebase Admin initialization
# (environment-based, deployment friendly)
# ---------------------------------------------------------

if not firebase_admin._apps:
    firebase_admin.initialize_app()


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split("Bearer ", 1)[1].strip()

    try:
        decoded = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = decoded.get("uid")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id


@router.get("/me")
def me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
