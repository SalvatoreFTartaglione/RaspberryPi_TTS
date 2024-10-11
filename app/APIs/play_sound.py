from fastapi import FastAPI, HTTPException, Form
from fastapi import APIRouter
from pathlib import Path
import os
import time
import subprocess
import threading
from database import database_helper as db

router = APIRouter()
ALLOWED_EXTENSIONS= {"mp3", "wav"}

stop_sound = False
repeat_sound = False
once = False
process_sound = []

# Function to play sound file
def play_sound(file_path: str, interval: int=0):
    """Function to play an audio file on MCU."""
    global stop_sound
    global repeat_sound
    global once
    global process_sound

    while stop_sound is False:
        process = subprocess.Popen(["mpg321", file_path], shell=False)
        process_sound.append(process)
        if once:
            if process.poll() is None:
               process.wait()
               process.terminate()
               break
            else:
               process.terminate()
               break

        elif repeat_sound:
          if process.poll() is None:
             process.wait()
             time.sleep(interval)
          if not process_sound:
            break
        else:
            break

    process_sound.clear()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API endpoint for playing a sound by position
@router.post("/playSoundByPosition/")
async def play_audio_by_pos(position: int = Form(1), repeat: bool = Form(True), interval: int=Form(3)):
    """Play an audio file with the option to repeat."""
    global repeat_sound
    global once
    global process_sound

    if not process_sound:
        if position is not None:
            if position < 1:
                raise HTTPException(status_code=400, detail="Invalid position.")
            else:
                sound = db.get_sound_by_pos(position)
        if repeat is False and interval>=1:
             raise HTTPException(status_code=400, detail="Interval is set correctly. Did you mean enable the repeat?")
        if repeat is True and (interval is None or interval<=0):
             raise HTTPException(status_code=400, detail="Invalid interval.")
        if sound is not None:
            # Construct the full file path
            file_path = Path(sound[3]).resolve()
            # Play the sound once or start repeating it
            if repeat:
                repeat_sound = True
                once = False
                repeat_thread = threading.Thread(target=play_sound, args=(file_path,interval,))
                repeat_thread.start()
                return {"status": f"Playing sound on repeat every {interval} seconds..."}
            else:
                # Play the sound once
                once = True
                repeat_sound = False
                thread = threading.Thread(target=play_sound, args=(file_path,))
                thread.start()
                return {"status": "Playing sound once..."}
        else:
            raise HTTPException(status_code=404, detail="No file at position: " + str(position))
    else:
        return {"status": "There is already a sound playing!"}


# API endpoint for playing a sound by position
@router.post("/playSoundByFileName/")
async def play_audio_by_filename(file_name: str = Form(...), repeat: bool = Form(False), interval: int = Form(None)):

    global repeat_sound
    global once
    global process_sound

    if not process_sound:
        # Check if file extension is valid
        if not allowed_file(file_name):
               raise HTTPException(status_code=400, detail="Invalid file format. Only .mp3 and .wav are allowed.")
        else:
               sound = db.get_sound_by_filename(file_name)
        if repeat is False and interval>=1:
             raise HTTPException(status_code=400, detail="Interval is set correctly. Did you mean enable the repeat?")
        if repeat is True and (interval is None or interval<=0):
             raise HTTPException(status_code=400, detail="Invalid interval.")

        if sound is not None:
            # Construct the full file path
            file_path = Path(sound[3]).resolve()

            # Play the sound once or start repeating it
            if repeat:
                repeat_sound = True
                once = False
                repeat_thread = threading.Thread(target=play_sound, args=(file_path, interval,))
                repeat_thread.start()
                return {"status": f"Playing sound on repeat every {interval} seconds."}
            else:
                # Play the sound once
                once = True
                repeat_sound = False
                thread = threading.Thread(target=play_sound, args=(file_path,))
                thread.start()
                return {"status": "Playing sound once..."}
        else:
            raise HTTPException(status_code=404, detail="No file at position: " + str(position))
    else:
        return {"status": "There is already a sound playing!"}


# API endpoint to stop audio playback
@router.post("/stopPlayback/")
def stop_playback():
    global stop_sound
    global process_sound
    global repeat_sound
    global once
    
    if process_sound:
         stop_sound = True
         if repeat_sound is True:
            repeat_sound = False
         for process in process_sound:
            process.terminate()
         process_sound = []
         stop_sound = False
         if once and not process.poll() is None:
            return {"status": "There is no sound playing"}
         else:            
            return {"status": "Sound stopped"}
    elif not process_sound:
         return {"status": "There is no sound playing"} 
