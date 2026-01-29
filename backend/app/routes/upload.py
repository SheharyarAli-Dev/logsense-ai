from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.parser import parse_log_file
from app.services.classifier import classify_log
from app.services.analyzer import analyze_root_cause
from app.services.solutions import suggest_solution

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
    
    analysis = analyze_root_cause(parsed_data)
    solutions = suggest_solution(analysis["root_cause"])


    return {
        "filename": file.filename,
        "total_logs": len(parsed_data),
        "analysis": analysis,
        "suggested_fixes": solutions,
        "sample_logs": parsed_data[:5]
    }
