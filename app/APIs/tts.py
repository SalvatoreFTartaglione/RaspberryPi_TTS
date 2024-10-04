from gtts import gTTS 
from fastapi import FastAPI, APIRouter
import os
import sqlite3
import subprocess
from pydantic import BaseModel
from database import database_helper as db

# Sound dir into Raspberry pi file system
UPLOAD_DIRECTORY = './soundPath/'
router = APIRouter()

# Model for request in JSON file
class TTSRequest(BaseModel):
	text: str
        
class TTSRequestAndSave(BaseModel):
	text: str
	file_name: str = None
        
# Reproduce text and save into file
@router.post("/ttsSave/")
async def tts(request: TTSRequestAndSave):
        # Creating tts file
        tts = gTTS(text=request.text, lang='it')
        # Save file into DIR
        if request.file_name is None :
                request.file_name = 'outputTTS' + str(db.get_latest_id()) + '.mp3'
        file_path = os.path.join(UPLOAD_DIRECTORY, request.file_name)
        tts.save(file_path)
        # Plays file
        subprocess.run(["mpg321", file_path])
        # Inserisce nel database e ottiene l'ID
        try:
                sound_id = db.set_sound(request.file_name, file_path)
        except sqlite3.IntegrityError as e:
                raise HTTPException(status_code=404, detail="Name already used. Try again with a different name")
        return {
                "id": sound_id,
                "file_name": request.file_name,
                "detail": "File uploaded successfully!"
                }
                        
# Reproduce message without saving into file
@router.post("/tts/")
async def tts(request: TTSRequest):
        # Creating tts file
        tts = gTTS(text=request.text, lang='it')
        temp_file = os.path.join(UPLOAD_DIRECTORY, "temp.mp3")
        tts.save(temp_file)
        # Plays file
        subprocess.run(["mpg321", temp_file])
        # Removes temp file
        os.remove(temp_file)
        return {"message": "Testo riprodotto"}
