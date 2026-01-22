from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.health import router as health_router
from api.tasks import router as tasks_router
from api.streaming import router as streaming_router

app = FastAPI(title="Mentra AI",version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router,prefix="/health",tags=["health"])
app.include_router(tasks_router,prefix="/tasks",tags=["tasks"])
app.include_router(streaming_router,prefix="/stream",tags=["streaming"])