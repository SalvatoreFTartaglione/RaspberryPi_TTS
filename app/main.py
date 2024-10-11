from fastapi import FastAPI
from pydantic import BaseModel
import threading
import uvicorn
from database import database_helper as db
from APIs.get_sound import router as get_sound_router
from APIs.upload_sound import router as upload_sound_router
from APIs.delete_sound import router as delete_sound_router
from APIs.play_sound import router as play_sound_router
from APIs.tts import router as tts_router
from APIs.reboot import router as reboot_router
from APIs.category import router as category_router

app = FastAPI()


app.include_router(get_sound_router)
app.include_router(upload_sound_router)
app.include_router(delete_sound_router)
app.include_router(play_sound_router)
app.include_router(tts_router)
app.include_router(reboot_router)
app.include_router(category_router)
db.create_table()
