
import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request

WINDOW_SECONDS = 60
MAX_REQUESTS = 60  # per user per window


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(deque)

    def check(self, key: str):
        now = time.time()
        q = self.requests[key]

        while q and q[0] <= now - WINDOW_SECONDS:
            q.popleft()

        if len(q) >= MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        q.append(now)


rate_limiter = RateLimiter()


def rate_limit(request: Request, user_id: str):
    key = f"{user_id}:{request.url.path}"
    rate_limiter.check(key)
