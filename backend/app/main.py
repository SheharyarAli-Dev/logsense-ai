from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="LogSense AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "LogSense AI Backend Running 🚀"}
