
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from audit.logger import audit_log
from utils.request_id import get_request_id

class ObservabilityMiddleware(BaseHTTPMiddleware):
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
