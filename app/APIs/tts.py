from gtts import gTTS
from fastapi import FastAPI, APIRouter, HTTPException, Form
import os
import sqlite3
import subprocess
from database import database_helper as db

# Sound dir into Raspberry pi file system
UPLOAD_DIRECTORY = './soundPath/'
ALLOWED_EXTENSIONS= {"mp3", "wav"}

router = APIRouter()

# Checks for allowed file extension in filename
def allowed_file(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

# API endpoint to produce text and save into file
@router.post("/tts/")
async def tts(text: str = Form(...), position: int = Form(None), file_name: str = Form(...), 
              category: str = Form(...) ):
    # Check if file extension is valid
    if not allowed_file(file_name):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .mp3 and .wav are allowed.")
    # Check if inserted category is valid
    if not db.category_is_valid(category):
        raise HTTPException(status_code=400, detail='Invalid Category Name')
    # Check if position is valid
    if position is not None and position < 1:
        raise HTTPException(status_code=400, detail="Invalid Position")
    # Checks if file already exists
    if db.get_sound_by_filename(file_name) is not None:
        raise HTTPException(status_code=400, detail='File Already Exists')
    
    # Creating tts file
    tts = gTTS(text=text, lang='it')
    
    # Save file into DIR
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    tts.save(file_path)
    
    # Insert into database
    try:
        position = db.set_sound(position, file_name, file_path, category)
    except sqlite3.IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Name already used. Try again with a different name")

    # Json response
    return {
        "position": position,
        "category": category,
        "file_name": file_name,
        "detail": "File uploaded successfully!"
    }
