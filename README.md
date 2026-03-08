# LogSense AI — Streamlit

Intelligent log analysis app built with Streamlit.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Click **New app**
4. Select your repo, branch, and set **Main file path** to `app.py`
5. Click **Deploy** — live in ~2 minutes

## Project Structure

```
logsense-streamlit/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme configuration
└── services/
    ├── parser.py           # Log file parser
    ├── classifier.py       # Keyword classifier
    ├── analyzer.py         # Root cause + trend analysis
    └── solutions.py        # Fix suggestions
```

## Expected Log Format

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

Accepted levels: `INFO`, `WARNING`, `ERROR`, `CRITICAL`
