# LogSense AI

**Intelligent Log Analysis Platform** — a full-stack system that parses, classifies, and diagnoses system logs, surfacing root causes, severity levels, and actionable fixes through a polished web dashboard.

---

## Overview

LogSense AI accepts uploaded `.log` files, processes them through a **five-stage pipeline**, and returns a rich JSON analysis. The backend is built with **FastAPI** and serves both the REST API and a self-contained static frontend. The frontend displays interactive charts, a sample log table, and detailed issue breakdowns.

---

## Features

- **Upload & Parse** – Accepts standard log files (`YYYY-MM-DD HH:MM:SS LEVEL Message` format).  
- **Weighted Keyword Classifier** – Scores messages across four issue categories (**Memory, Crash, Disk, Network**).  
- **Root Cause Analysis** – Aggregates categories with importance multipliers to determine the dominant issue.  
- **Severity Assignment** – Critical, High, Medium, or Low based on issue composition.  
- **Trend Analysis** – Groups issues into 10‑minute buckets for time‑series visualisation.  
- **Rich Frontend** – Built into a single `index.html`:
  - Animated file upload with spinner and toasts
  - Doughnut chart of issue distribution
  - Line chart of trends
  - Sample logs table with category highlighting
  - Responsive, dark‑mode design
- **CORS** – Open for development (*), easily lockable for production

---

## Quick Start

### Clone the repository


git clone https://github.com/yourusername/logsense-ai.git
cd logsense-ai/backend
Install dependencies

Currently requirements.txt is empty, so install manually:

pip install fastapi uvicorn python-multipart
Run the server
uvicorn app.main:app --reload --port 8000
Open the dashboard

Visit http://localhost:8000
 and upload a .log file.

Test with cURL
curl -X POST http://localhost:8000/upload-log \
  -F "file=@logs/test.log"
API Reference

POST /upload-log

Accepts a multipart form upload of a .log file and returns analysis results.

Request

file: The log file (.log extension required)

Response (JSON)

{
  "filename": "test.log",
  "total_logs": 56,
  "analysis": {
    "root_cause": "Crash Issue",
    "severity": "Critical",
    "issue_count": {
      "Memory Issue": 6,
      "Crash Issue": 4,
      "Network Issue": 4,
      "Disk Issue": 3
    }
  },
  "trends": {
    "2026-01-27 09:00:00": { "Normal": 3, "Memory Issue": 1 },
    "2026-01-27 09:10:00": { "Crash Issue": 2, "Normal": 2 }
  },
  "suggested_fixes": [
    "Inspect application crash logs",
    "Restart the service",
    "Check recent code deployments"
  ],
  "sample_logs": [ ... ]
}

Error cases

{"error": "Only .log files are allowed"} – file extension not .log

{"root_cause": "No major issues detected", "severity": "Low", "issue_count": {}} – clean log

{"suggested_fixes": ["No suggestion available"]} – unknown root cause

Architecture

The system runs on a single FastAPI server that hosts both the API and static frontend.

Browser → FastAPI (main.py) → routes/upload.py
         ↓
    services/parser.py    (parsing & classification)
    services/analyzer.py  (root cause, severity, trends)
    services/solutions.py (fix suggestions)
         ↓
    JSON response → Browser

Static frontend is mounted at / from app/static/index.html.

Uploaded logs are saved to the logs/ directory (local filesystem).

CORS is wide-open for development – restrict in production.

Classifier Logic

Each log message is scored against weighted keyword dictionaries. The category with the highest cumulative score wins; if no keywords match, the message is classified as Normal.

Category	Keywords (weights)	Max score
Memory Issue	memory×3, ram×2, heap×2, leak×4, overflow×4	15
Crash Issue	crash×4, failed×3, fatal×5, shutdown×3, terminated×4	19
Disk Issue	disk×3, storage×2, space×2, full×4, write error×3	14
Network Issue	timeout×3, connection×2, unreachable×4, refused×3, network×2	14

Code excerpt (from services/parser.py)

def classify_log_message(message: str):
    message_lower = message.lower()
    scores = {}
    for issue, keywords in ISSUE_KEYWORDS.items():
        score = 0
        for word, weight in keywords.items():
            if word in message_lower:
                score += weight
        if score > 0:
            scores[issue] = score
    return max(scores, key=scores.get) if scores else "Normal"
Severity Levels

After collecting issue counts, an overall severity is assigned:

Critical – Any crash issue present in the logs

High – Two or more memory issues

Medium – Three or more total issues of any type

Low – Fewer than three issues and no crashes

Importance multipliers for root cause selection

Crash Issue ×3

Memory Issue ×2

Disk Issue ×2

Network Issue ×2

General Error ×1

Project Structure
logsense-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry, mounts static files
│   │   ├── routes/
│   │   │   └── upload.py           # POST /upload-log handler
│   │   ├── services/
│   │   │   ├── parser.py           # Parsing + classification
│   │   │   ├── classifier.py       # (empty – legacy/incorrect)
│   │   │   ├── analyzer.py         # Root cause, severity, trends
│   │   │   └── solutions.py        # Suggestion lookup
│   │   └── static/
│   │       ├── index.html          # Full frontend
│   │       ├── js/upload.js        # Legacy (unused)
│   │       └── css/style.css       # Legacy (unused)
│   ├── logs/
│   │   └── test.log                # Sample log with 56 entries
│   └── requirements.txt            # (empty)
Known Issues
ID	Severity	Description
BUG‑001	High	Classifier outputs "Disk Issue" but solutions dictionary uses "Storage Issue" – disk logs always get "No suggestion".
BUG‑002	High	requirements.txt is empty; dependencies must be installed manually.
BUG‑003	Medium	Classifier code lives in parser.py while classifier.py is empty – separation of concerns broken.
BUG‑004	Medium	Open CORS policy (allow_origins=["*"]) – acceptable for dev, risky in production.
BUG‑005	Medium	No file size limit on upload – large files could exhaust server resources.
BUG‑006	Medium	Missing .critical CSS class – severity badge for Critical level is unstyled.
BUG‑007	Low	GET / route defined in main.py is shadowed by StaticFiles – unreachable.
BUG‑008	Low	Legacy static files (js/upload.js, css/style.css) are unused and can be removed.
License

This project is provided for demonstration purposes.
