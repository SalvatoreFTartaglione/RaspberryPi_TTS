from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi import APIRouter
from pathlib import Path
from database import database_helper as db
import os

# sound dir into Raspberry Pi file system
router = APIRouter()


# API endpoint to get a list sounds
@router.get("/getSoundsList/")
def list_audio_files():
    list=db.get_sounds_list()
    # Check if list id empty
    if list:
       file_response = []
       for elem in list:
           # returns json with list
           file_response.append({"position": elem[1], "file_name": elem[2], "category": elem[4]})
       file_response.sort(key=lambda x: x["position"])
       return file_response
    # if list is empty
    if not list:
       raise HTTPException(status_code=400, detail="Empty List")
    else:
       raise HTTPException(status_code=400, detail="Invalid Request")


# API endpoint to get a list of sound by speified category
@router.get("/getSoundsListByCategory/")
def list_audio_files_by_category(category: str):
    list=db.get_sounds_list_by_category(category)
    # Checks if category inserted by user exists
    if not db.category_is_valid(category):
       raise HTTPException(status_code=400, detail='Invalid Category Name')
    # Checks if category has sounds	
    if list:
        file_response = []
        for elem in list:
            # Returns json with list
            file_response.append({"position": elem[1], "file_name": elem[2], "category": elem[4]})
        file_response.sort(key=lambda x: x["position"])
        return file_response
    if not list:
        raise HTTPException(status_code = 400, detail = 'No Sounds in ' + str(category))
    else:
        raise HTTPException(status_code = 400, detail = 'Bad Request')


# API endpoint to get soound by ID  
@router.get("/getSoundByPosition/")
def get_sound(pos: str):
    sound = db.get_sound_by_pos(pos)    
    if sound is not None:
        return FileResponse(path=sound[3], media_type='audio/mpeg', filename=sound[2])
    else:
        raise HTTPException(status_code=404, detail="File not found")
        return
    

# API endpoint to get sound by file_name
@router.get("/getSoundByFileName/")
def get_sound(file_name: str):
    sound = db.get_sound_by_filename(file_name)
    if sound is not None:
        return FileResponse(path=sound[3], media_type="audio/mpeg", filename=sound[2])
    else:
        raise HTTPException(status_code=404, detail="File not found")
        return

