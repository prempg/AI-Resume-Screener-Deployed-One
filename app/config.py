import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

    MONGO_URI: str = os.getenv(
        "MONGO_URI",
        "mongodb://admin:admin@mongo:27017",
    )

    REDIS_HOST: str = os.getenv("REDIS_HOST", "valkey")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/mnt/uploads")

    GROQ_TEXT_MODEL: str = os.getenv(
        "GROQ_TEXT_MODEL",
        "llama-3.3-70b-versatile",
    )

    GROQ_VISION_MODEL: str = os.getenv(
        "GROQ_VISION_MODEL",
        "meta-llama/llama-4-scout-17b-16e-instruct",
    )


settings = Settings()
