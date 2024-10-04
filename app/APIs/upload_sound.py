from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi import APIRouter
import os
import shutil
from database import database_helper as db 

router = APIRouter()

UPLOAD_DIRECTORY = './soundPath/'
ALLOWED_EXTENSIONS = {"mp3", "wav"}

# Crea la tabella al primo avvio
#db.create_table()

# Crea la cartella se non esiste
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/uploadSound/")
async def upload_file(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .mp3 and .wav are allowed.")
        
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    # Salva il file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Inserisce nel database e ottiene l'ID
    sound_id = db.set_sound(file.filename, file_location)
    return {
        "id": sound_id,
        "filename": file.filename,
        "detail": "File uploaded successfully!"
        }
