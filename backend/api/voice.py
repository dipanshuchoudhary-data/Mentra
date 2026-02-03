
from fastapi import APIRouter, UploadFile, File, Depends
from backend.stt.transcribe import SpeechToTextService
from backend.api.dependencies import guarded
from backend.core.task_manager import TaskManager

router = APIRouter()
stt = SpeechToTextService()
task_manager = TaskManager()

@router.post("/transcribe-and-create")
async def transcribe_and_create(
    audio: UploadFile = File(...),
    user_id: str = Depends(guarded),
):
    audio_bytes = await audio.read()
    text = stt.transcribe_wav(audio_bytes)

    task = task_manager.create_task(
        user_id=user_id,
        message=text,
    )

    return {
        "transcript": text,
        "task": task.model_dump(),
    }
