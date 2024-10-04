from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import APIRouter
import os
from pathlib import Path
import shutil
from database import database_helper as db

router = APIRouter()

# Deletes sound by file_name
@router.delete("/deleteSoundByFileName/{file_name}")
async def delete_sound_by_file_name(file_name: str):
    # if file exists delete it
    if db.check_sound_by_filename(file_name):
        path = Path(db.get_sound_by_filename(file_name)[2]).resolve()
        # Remove file from fily system
        os.remove(path)  
        # Remove from database
        db.delete_sound_by_filename(file_name)
        return {"detail": f"File '{file_name}' deleted successfully."}
    # Otherwise return warning (404)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return 

# Deletes sound by id
@router.delete("/deleteSoundById/{id}")
async def delete_sound_by_id(id: str):
    # if file exists delete it
    if db.check_sound_by_id(id):
        file_name = db.get_sound_by_id(id)[1]
        path = Path(db.get_sound_by_id(id)[2]).resolve()
        # Remove file from fily system
        os.remove(path)  
        # Remove entry from database
        db.delete_sound_by_id(id)
        return {"detail": f"File '{file_name}' deleted successfully."}
    # Otherwise return warning (404)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return 
