from fastapi import FastAPI, HTTPException, Response, Form
from fastapi.responses import FileResponse
from fastapi import APIRouter
import sqlite3
from pathlib import Path
from database import database_helper as db
import os

router = APIRouter()


# API endpoint to get a category list
@router.get("/getCategoryList/")
def list_categories():

    list=db.get_category_list()
    # Checks if list is empty
    if list:
       file_response = []
       for elem in list:
           # Returns json with list
           file_response.append({"category_name": elem[0]})
       file_response.sort(key=lambda x: x["category_name"])
       return file_response
    # if list is empty
    if not list:
       raise HTTPException(status_code=400, detail="Empty category list")
    else:
       raise HTTPException(status_code=400, detail="Invalid Request")


# API endpoint to insert a new category
@router.post("/setCategory/")
def set_category(category: str=Form(...)):

    # Transform input into lower case and trims
    category = category.lower()
    category = category.strip()
    # Input controls
    if len(category) > 17:
        raise HTTPException(status_code=400, detail="Insert a shorter category name")
    if db.category_is_valid(category):
        raise HTTPException(status_code=400, detail="Category name already used")     
    # Insert category into db
    try:
        db.set_category(category)
        return {'Category ' + str(category) + ' created succesfully'}
    except sqlite3.IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="An Error occured")


# API endpoint to delete a category by its name
@router.delete("/deleteCategory/")
def delete_category(category: str=Form(...)):

    # Trasform input into lower case and trims 
    category = category.lower()
    category = category.strip()
    #Input control   
    if not db.category_is_valid(category):
        raise HTTPException(status_code=400, detail="Category does not exist")
    # Check whether there are still sound for the specified category
    if db.get_sounds_list_by_category(category):
        raise HTTPException(status_code=400, detail="Cannot delete: " + str(category) +" there are still sounds within category")
    # Delete category
    try:
        db.delete_category(category)
        return {str(category) + ' deleted succesfully'}
    except sqlite3.IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="An Error occurred")
