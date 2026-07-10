import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base Configuration"""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "hospital-secret-key")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hospital.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload Settings
    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Session
    SESSION_PERMANENT = False

    # Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Timezone
    TIMEZONE = "Asia/Kolkata"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}