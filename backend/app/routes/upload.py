from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.parser import parse_log_file
from app.services.classifier import classify_log

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
    
    for log in parsed_data:
        log["category"] = classify_log(log)

    return {
        "filename": file.filename,
        "total_logs": len(parsed_data),
        "classified_logs": parsed_data[:5]
    }
