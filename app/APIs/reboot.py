from fastapi import FastAPI, HTTPException, APIRouter
import os
import subprocess

router = APIRouter()

# API endpoint to reboot system
@router.post("/reboot/")
def reboot_system():
    try:
        subprocess.run(['sudo', 'reboot'], check=True)
        return {"message": "Rebooting the system..."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to reboot the system: {str(e)}")
