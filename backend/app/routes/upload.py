from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "logs"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith(".log"):
        return {"error": "Only .log files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "Log file uploaded successfully"
    }
