from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi import APIRouter
from pathlib import Path
from database import database_helper as db
import os

'''GESTIRE NOME SOUND ERRATO IN HTTP REQUEST E ID ERRATO CON ECCEZIONI'''

# sound dir into Raspberry Pi file system
router = APIRouter()

# Funzione per ottenere i nomi dei file audio disponibili nella directory
# API to get list sounds
@router.get("/getSoundsList/")
def list_audio_files():
    list=db.get_sounds_list();
    file_response = []
    for elem in list:
        # restituisce la lista dei file disponibili
        file_response.append({"id": elem[0], "filename": elem[1]})
    return file_response

# API endpoint to get soound by ID  
@router.get("/getSoundById/")
def get_sound(id: str):
    if db.check_sound_by_id(id):
        # Sanifica l'input eliminando potenziali exploit
        if ".." in id or "/" in id or "\\" in id:
            raise HTTPException(status_code=400, detail="Invalid Request")
        # Get sound from database
        path = db.get_sound_by_id(id)[2]
        file_path = Path(path).resolve() 
        return FileResponse(file_path, media_type="audio/mpeg", filename=db.get_sound_by_id(id)[1])
    else:
        raise HTTPException(status_code=404, detail="File not found")
        return
    

# API endpoint to get sound by file_name
@router.get("/getSoundByFileName/")
def get_sound(file_name: str):
    if db.check_sound_by_filename(file_name):
        # Sanifica l'input eliminando potenziali exploit
        if ".." in file_name or "/" in file_name or "\\" in file_name:
            raise HTTPException(status_code=400, detail="Invalid Request")
        # Get sound from database
        path = db.get_sound_by_filename(file_name)[2]
        file_path = Path(path).resolve() 
        return FileResponse(file_path, media_type="audio/mpeg", filename=db.get_sound_by_filename(file_name)[1])
    else:
        raise HTTPException(status_code=404, detail="File not found")
        return

