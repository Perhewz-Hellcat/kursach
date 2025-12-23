import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:123456789@localhost:5432/audio_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")

    UPLOAD_FOLDER = "uploads/audio"
    ALLOWED_EXTENSIONS = {"wav", "mp3", "flac", "ogg"}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
