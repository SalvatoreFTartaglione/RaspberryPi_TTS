from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi import APIRouter
import os
import shutil
import sqlite3
from database import database_helper as db 

router = APIRouter()

UPLOAD_DIRECTORY = './soundPath/'
ALLOWED_EXTENSIONS = {"mp3", "wav"}

#  if UPLOAD_DIRECTORY does not exist it creates the dir
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Checks allowed file extension
def allowed_file(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# API endpoint to upload a sound 
@router.post("/uploadSound/")
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form(...),
    position: int = Form(None)
):
    # Check file extension
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .mp3 and .wav are allowed.")
            
    # Check if file_name is already into db
    if db.get_sound_by_filename(file.filename) :
        raise HTTPException(status_code=400, detail="File Already Exists")

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Check if request position is invalid
    if position is not None:
        if position < 1:
            raise HTTPException(status_code=400, detail="Invalid Position.")

    try:
        # Insert sound into db
        position = db.set_sound(position, file.filename, file_location, category)
        return {
            "file_name": file.filename,
            "position": position,
            "category": category,
            "detail": "File uploaded successfully!"
        }
    except sqlite3.IntegrityError as e:
        error_message = str(e)
        print(e)
        # Input validation
        if "UNIQUE constraint failed: SOUND.file_path" in error_message:
            raise HTTPException(status_code=400, detail="Name already used. Try again with a different name.")
        elif "FOREIGN KEY constraint failed" in error_message:
            raise HTTPException(status_code=400, detail="Category name doesn't exist.")
        else:
            raise HTTPException(status_code=400, detail="Integrity error occurred.")

