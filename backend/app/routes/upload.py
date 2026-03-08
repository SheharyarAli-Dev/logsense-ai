from fastapi import APIRouter, UploadFile, File
import io
from app.services.parser import parse_log_file
from app.services.classifier import classify_log_message
from app.services.analyzer import analyze_root_cause, analyze_trends
from app.services.solutions import suggest_solution

router = APIRouter()

@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".log"):
        return {"error": "Only .log files are allowed"}

    # Read uploaded file into memory
    contents = await file.read()
    file_like = io.BytesIO(contents)

    # Parse logs
    parsed_data = parse_log_file(file_like)
    
    # Classify each log message
    for log in parsed_data:
        log["category"] = classify_log_message(log["message"])
    
    # Analyze logs
    analysis = analyze_root_cause(parsed_data)
    solutions = suggest_solution(analysis["root_cause"])
    trends = analyze_trends(parsed_data, interval_minutes=10)

    # Return JSON response
    return {
        "filename": file.filename,
        "total_logs": len(parsed_data),
        "analysis": analysis,
        "trends": trends,
        "suggested_fixes": solutions,
        "sample_logs": parsed_data[:15]
    }
