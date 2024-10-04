from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import threading
import uvicorn
from database import database_helper as db
from APIs.get_sound import router as get_sound_router
from APIs.upload_sound import router as upload_sound_router
from APIs.delete_sound import router as delete_sound_router
from APIs.play_sound import router as play_sound_router
from APIs.tts import router as tts_router
from APIs.reboot import router as reboot_router

app = FastAPI()


app.include_router(get_sound_router)
app.include_router(upload_sound_router)
app.include_router(delete_sound_router)
app.include_router(play_sound_router)
app.include_router(tts_router)
app.include_router(reboot_router)
db.create_table()
#Starts Dash into a separate thread
#def start_dash_app():
    #dash_app = create_dash_app()
    #ash_app.run_server(host="0.0.0.0", port=8050)

#if __name__ == "__main__":
    #Starts Dash into a separate thread
    #dash_thread = threading.Thread(target=start_dash_app)
    #dash_thread.start()
    # Starts FastAPI with uviCorn into a separate thread
    #uvicorn.run(app, host="0.0.0.0", port=8000)
