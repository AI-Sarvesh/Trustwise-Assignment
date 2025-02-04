from typing import Dict, ClassVar, List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Trustwise Text Analysis API"
    BASE_DIR: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL: str = "sqlite:///./analysis.db"
    FRONTEND_URL: str = "http://localhost:5173"
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:5173", "http://frontend:5173"]
    MODELS: ClassVar[Dict[str, str]] = {
        'emotion': 'SamLowe/roberta-base-go_emotions',
        'vectara': 'vectara/hallucination_evaluation_model'
    }
    SECRET_KEY: str = "your-secret-key"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
        return self.CORS_ORIGINS

settings = Settings() 