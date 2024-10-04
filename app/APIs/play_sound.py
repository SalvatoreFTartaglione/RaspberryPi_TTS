from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pathlib import Path
import os
import time
import subprocess 
import threading  
from pydantic import BaseModel
from database import database_helper as db

router = APIRouter()

#model for requests in json file
class AudioRequestByFileName(BaseModel):
    file_name: str
    repeat: bool = False

class AudioRequestById(BaseModel):
    id: str
    repeat: bool = False
        
# Function to play sound file
def play_sound(file_path: str):
    """Function to play an audio file on MCU."""
    print('playing sound') 
    subprocess.run(['mpg321', file_path], check=True)
    
# Background function to repeat the sound
def repeat_sound(file_path: str, interval: int = 2):
    """Function to repeat the sound every 'interval' seconds."""
    while True:
        play_sound(file_path)
        time.sleep(interval)

# API endpoint for playing a sound by file_name
@router.post("/playSoundByFileName/")
async def play_audio_by_file_name(request: AudioRequestByFileName):                   
    """Play an audio file with the option to repeat."""
    if db.check_sound_by_filename(request.file_name):
        sound = db.get_sound_by_filename(request.file_name)
        repeat = request.repeat
        # Construct the full file path
        file_path = Path(sound[2]).resolve() 
        # Play the sound once or start repeating it
        if repeat:
            # Start a new thread to repeat the sound
            repeat_thread = threading.Thread(target=repeat_sound, args=(file_path,))
            repeat_thread.start()
            return {"status": "Playing sound on repeat every 5 seconds."}
        else:
            # Play the sound once
            play_sound(file_path)
            return {"status": "Playing sound once."}
    else: 
        raise HTTPException(status_code=404, detail="File not found")
        return 
            
# API endpoint for playing a sound by id
@router.post("/playSoundById/")
async def play_audio_by_id(request: AudioRequestById):                   
    """Play an audio file with the option to repeat."""
    if db.check_sound_by_id(request.id) : 
        sound = db.get_sound_by_id(request.id)
        repeat = request.repeat
        # Construct the full file path
        file_path = Path(sound[2]).resolve() 
        # Play the sound once or start repeating it
        if repeat:
            # Start a new thread to repeat the sound
            repeat_thread = threading.Thread(target=repeat_sound, args=(file_path,))
            repeat_thread.start()
            return {"status": "Playing sound on repeat every 5 seconds."}
        else:
            # Play the sound once
            play_sound(file_path)
            return {"status": "Playing sound once."}
    else:
        raise HTTPException(status_code=404, detail="File not found")
        return
