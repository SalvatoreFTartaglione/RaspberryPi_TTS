from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import APIRouter
import os
from pathlib import Path
import shutil
from database import database_helper as db

router = APIRouter()
ALLOWED_EXTENSIONS = {"mp3", "wav"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
# Deletes sound by file_name
@router.delete("/deleteSoundByFileName/{file_name}")
async def delete_sound_by_file_name(file_name: str):

    # Checks file extension
    if not allowed_file(file_name):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .mp3 and .wav are allowed.")
    sound = db.get_sound_by_filename(file_name)

    # if file exists delete it
    if sound is not None:
        path = Path(sound[3]).resolve()
        # Remove file from fily system
        os.remove(path)
        # Remove from database
        db.delete_sound_by_filename(file_name)
        return {"detail": f"File '{file_name}' deleted successfully."}
    # Otherwise return warning (404)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return 

# Deletes sound by position
@router.delete("/deleteSoundByPosition/{position}")
async def delete_sound_by_id(position: int):
    # Checks if inserted postion is valid
    if position is not None:
        if position < 1:
            raise HTTPException(status_code=400, detail="Invalid Position.")
    sound = db.get_sound_by_pos(position)
    # if file exists delete it
    if sound is not None:
        file_name = sound[2]
        path = Path(sound[3]).resolve()
        # Remove file from fily system
        os.remove(path)  
        # Remove entry from database
        db.delete_sound_by_pos(position)
        return {"detail": f"File '{file_name}' in position '{position}' deleted successfully."}
    # Otherwise return warning (404)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return 
