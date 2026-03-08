# LogSense AI

<div align="center">

![LogSense AI](https://img.shields.io/badge/LogSense-AI-6C63FF?style=for-the-badge&logoColor=white)
![Netlify](https://img.shields.io/badge/Deployed_on-Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Intelligent log analysis platform that parses, classifies, and diagnoses system logs — surfacing root causes, severity levels, and actionable fixes through a polished web dashboard.**

[🚀 Live Demo](https://ai-powered-log-analyzer.netlify.app/) · [Report Bug](https://github.com/yourusername/logsense-ai/issues) · [Request Feature](https://github.com/yourusername/logsense-ai/issues)

</div>

---

## 📸 Preview

> Upload a `.log` file → get instant root-cause analysis, severity rating, suggested fixes, and interactive charts.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **File Upload** | Drag-and-drop or browse for `.log` files |
| 🔍 **Log Parser** | Extracts `timestamp`, `level`, and `message` from standard log format |
| 🧠 **Weighted Classifier** | Scores messages across 4 categories — Memory, Crash, Disk, Network |
| 🎯 **Root Cause Analysis** | Aggregates issue categories with priority multipliers |
| 🚨 **Severity Rating** | Assigns Critical, High, Medium, or Low based on issue composition |
| 📈 **Trend Analysis** | Groups issues into 10-minute time buckets for time-series visualisation |
| 📊 **Interactive Charts** | Doughnut chart (category distribution) + Line chart (issue trends) |
| 💡 **Suggested Fixes** | Actionable remediation steps per root cause |
| 🌙 **Dark UI** | Responsive, polished dashboard — no framework needed |

---

## 🏗️ Architecture

```
logsense-ai/
├── netlify.toml                    # Netlify config & /api/* redirect rules
├── package.json                    # Root-level dependencies (busboy)
├── public/
│   └── index.html                  # Full frontend (HTML + CSS + JS)
└── netlify/
    └── functions/
        └── upload-log.js           # Serverless backend — all analysis logic
```

The entire backend runs as a single **Netlify serverless function**. No dedicated server, no Python runtime, no external API needed.

---

## 🔬 How It Works

The analysis runs through a **5-stage pipeline** on every uploaded file:

```
.log file  →  Parser  →  Classifier  →  Analyzer  →  Solutions  →  JSON response
```

### Stage 1 — Parser
Reads each line and extracts structured fields using a regex pattern:
```
2024-01-15 10:01:22  ERROR  Memory leak detected in heap allocation
└─ timestamp ──────┘ └────┘ └─ message ──────────────────────────┘
                      level
```
Lines that don't match (blank lines, stack traces) are silently ignored.

### Stage 2 — Weighted Keyword Classifier
Each message is scored against keyword lists. The category with the highest total score wins:

| Category | Keywords & Weights |
|---|---|
| 🟡 Memory Issue | `leak` ×4, `overflow` ×4, `memory` ×3, `heap` ×2, `ram` ×2 |
| 🔴 Crash Issue | `fatal` ×5, `terminated` ×4, `crash` ×4, `failed` ×3, `shutdown` ×3 |
| 🟠 Disk Issue | `full` ×4, `disk` ×3, `write error` ×3, `storage` ×2, `space` ×2 |
| 🔵 Network Issue | `unreachable` ×4, `refused` ×3, `timeout` ×3, `network` ×2, `connection` ×2 |
| ⚪ Normal | No keywords matched |

### Stage 3 — Root Cause Analyzer
Counts all classified issues and applies importance multipliers to find the dominant problem:

```
Crash Issue   × 3  (highest priority)
Memory Issue  × 2
Disk Issue    × 2
Network Issue × 2
General Error × 1
```

### Stage 4 — Severity Assignment

| Severity | Condition |
|---|---|
| 🔴 **Critical** | Any Crash Issue detected |
| 🟠 **High** | 2 or more Memory Issues |
| 🟡 **Medium** | 3 or more total issues |
| 🟢 **Low** | Everything else |

### Stage 5 — Trend Analysis
Logs are grouped into 10-minute time buckets to build the time-series data powering the trends chart.

---

## 🚀 Quick Start

### Prerequisites
- [Node.js](https://nodejs.org/) v16+
- [Netlify CLI](https://docs.netlify.com/cli/get-started/) (for local dev)

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/logsense-ai.git
cd logsense-ai

# 2. Install dependencies
npm install

# 3. Install Netlify CLI globally
npm install -g netlify-cli

# 4. Start local dev server
netlify dev
```

Visit `http://localhost:8888` and upload a `.log` file.

---

## 📡 API Reference

### `POST /api/upload-log`

Accepts a multipart form upload of a `.log` file and returns a full analysis.

**Request**
```bash
curl -X POST https://ai-powered-log-analyzer.netlify.app/api/upload-log \
  -F "file=@your-file.log"
```

**Response**
```json
{
  "filename": "app.log",
  "total_logs": 42,
  "analysis": {
    "root_cause": "Crash Issue",
    "severity": "Critical",
    "issue_count": {
      "Crash Issue": 3,
      "Memory Issue": 2
    }
  },
  "suggested_fixes": [
    "Inspect application crash logs",
    "Restart the service",
    "Check recent code deployments"
  ],
  "trends": {
    "2024-01-15 10:00:00": { "Crash Issue": 2, "Normal": 5 },
    "2024-01-15 10:10:00": { "Memory Issue": 1, "Normal": 3 }
  },
  "sample_logs": [
    {
      "timestamp": "2024-01-15 10:01:22",
      "level": "ERROR",
      "message": "Memory leak detected in heap allocation",
      "category": "Memory Issue"
    }
  ]
}
```

**Supported log format**
```
YYYY-MM-DD HH:MM:SS  LEVEL  Message text here
```
Where `LEVEL` is one of: `INFO`, `WARNING`, `ERROR`, `CRITICAL`

---

## 🧪 Test It Out

Don't have a log file? Paste this into a file called `test.log`:

```
2024-01-15 10:00:01 INFO Application started successfully
2024-01-15 10:01:22 ERROR Memory leak detected in heap allocation
2024-01-15 10:02:45 CRITICAL Application crash detected - fatal error
2024-01-15 10:03:10 WARNING Connection timeout on port 8080
2024-01-15 10:04:33 ERROR Failed to write to disk - storage full
2024-01-15 10:06:14 ERROR Memory overflow in buffer
2024-01-15 10:07:22 CRITICAL Service terminated unexpectedly
```

**Expected result:** Root Cause → `Crash Issue` · Severity → `Critical`

---

## 🚢 Deployment

### Deploy to Netlify (one click)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/logsense-ai)

### Manual deploy via Netlify CLI

```bash
netlify deploy --prod
```

### Via Netlify Dashboard (drag & drop)
1. Go to [app.netlify.com](https://app.netlify.com)
2. Drag the project folder onto the deploy area
3. Done ✓

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 · CSS3 · Vanilla JavaScript |
| Charts | [Chart.js](https://www.chartjs.org/) |
| Backend | Netlify Serverless Functions (Node.js) |
| File Parsing | [busboy](https://github.com/mscdex/busboy) |
| Hosting | [Netlify](https://netlify.com) |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
Made with ☕ · <a href="https://ai-powered-log-analyzer.netlify.app/">Live Demo</a>
</div>
