from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from backend.audit.logger import audit_log
from backend.utils.request_id import get_request_id

from firebase_admin import auth as firebase_auth


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    This middleware now does TWO things:

    1. Request observability (already existed)
    2. Firebase identity verification (Phase-2 requirement)

    After this middleware runs:

        request.state.user_id  -> ALWAYS contains the Firebase UID

    If the token is missing or invalid, the request is rejected.
    """

    # Endpoints that should not require authentication
    # (keep this minimal)
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
        # Phase 2 – Firebase identity verification
        # ---------------------------------------------------------

        request.state.user_id = None

        if request.url.path not in self._PUBLIC_PATHS:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing Authorization token")

            id_token = auth_header.split("Bearer ", 1)[1].strip()

            try:
                decoded_token = firebase_auth.verify_id_token(id_token)
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid Firebase token")

            user_id = decoded_token.get("uid")

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid Firebase token payload")

            # Attach trusted identity to request context
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
