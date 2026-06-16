from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "E-Commerce API"))

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the E-Commerce Backend!",
        "status": "Healthy",
        "debug_mode": os.getenv("DEBUG")
    }