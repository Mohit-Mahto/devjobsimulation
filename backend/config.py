import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use localhost if MONGO_URI is not provided
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/devjob")
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-default-key")
    JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "")
    JUDGE0_URL = os.getenv("JUDGE0_URL", "https://judge0-ce.p.rapidapi.com")
