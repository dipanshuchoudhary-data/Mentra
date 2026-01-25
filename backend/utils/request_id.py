import uuid
from fastapi import Request

def get_request_id(request:Request) -> str:
    rid = request.headers.get("X-request-ID")
    return rid if rid else str(uuid.uuid4())