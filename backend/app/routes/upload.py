from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.parser import parse_log_file

router = APIRouter()

UPLOAD_DIR = "logs"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith(".log"):
        return {"error": "Only .log files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed_data = parse_log_file(file_path)

    return {
        "filename": file.filename,
        "total_lines_parsed": len(parsed_data),
        "logs": parsed_data[:5]  
    }
