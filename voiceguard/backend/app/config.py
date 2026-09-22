from typing import List, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "VoiceGuard AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "voiceguard-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    DATABASE_URL: str = "sqlite:///./voiceguard.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"]

    # AI & Audio Processing Configs
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHUNK_DURATION_SEC: float = 2.0
    AUDIO_OVERLAP_SEC: float = 0.5
    WHISPER_MODEL_SIZE: str = "base"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"
    DEEPFAKE_MODEL_NAME: str = "Hyperion/wav2vec2-base-asvspoof"
    SPEAKER_MODEL_NAME: str = "speechbrain/spkrec-ecapa-voxceleb"

    # Risk Fusion Weights (Must sum to 1.0)
    WEIGHT_DEEPFAKE: float = 0.30
    WEIGHT_SPEAKER_MISMATCH: float = 0.25
    WEIGHT_SOCIAL_ENG: float = 0.25
    WEIGHT_TRANSACTION_RISK: float = 0.15
    WEIGHT_CONTEXT_RISK: float = 0.05

    # Risk Score Thresholds (0-100)
    THRESHOLD_LOW: float = 30.0
    THRESHOLD_MEDIUM: float = 50.0
    THRESHOLD_HIGH: float = 75.0
    THRESHOLD_CRITICAL: float = 85.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
