import os

class Config:
    JWT_SECRET = os.getenv("JWT_SECRET", "fallback_default_key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")