from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from backend.audit.logger import audit_log
from backend.utils.request_id import get_request_id

import firebase_admin
from firebase_admin import auth as firebase_auth


# ---------------------------------------------------------
# Firebase Admin initialization
# (environment-based, deployment friendly)
# ---------------------------------------------------------

if not firebase_admin._apps:
    firebase_admin.initialize_app()


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    - request observability
    - Firebase authentication
    - attaches request.state.user_id
    """

    _PUBLIC_PATHS = {
        "/health",
    }

    async def dispatch(self, request: Request, call_next):
        request_id = get_request_id(request)
        request.state.request_id = request_id

        audit_log(
            task_id="SYSTEM",
            event="REQUEST_IN",
            meta={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        # ---------------------------------------------------------
        # Firebase identity verification
        # ---------------------------------------------------------

        request.state.user_id = None

        if request.url.path not in self._PUBLIC_PATHS:

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401,
                    detail="Missing Authorization token",
                )

            id_token = auth_header.split("Bearer ", 1)[1].strip()

            try:
                decoded_token = firebase_auth.verify_id_token(id_token)
            except Exception as e:
                # Temporary debug (you can remove later)
                print("FIREBASE VERIFY ERROR:", repr(e))
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Firebase token",
                )

            user_id = decoded_token.get("uid")

            if not user_id:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Firebase token payload",
                )

            request.state.user_id = user_id

        # ---------------------------------------------------------

        response = await call_next(request)

        audit_log(
            task_id="SYSTEM",
            event="REQUEST_OUT",
            meta={
                "request_id": request_id,
                "status_code": response.status_code,
            },
        )

        response.headers["X-Request-ID"] = request_id
        return response
