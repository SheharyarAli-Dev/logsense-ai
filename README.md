# LogSense AI 

Intelligent Log Analysis Platform — a full-stack system that parses, classifies, and diagnoses system logs, surfacing root causes, severity levels, and actionable fixes through a polished web dashboard. 

Link: https://ai-log-analyzer.netlify.app/

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


