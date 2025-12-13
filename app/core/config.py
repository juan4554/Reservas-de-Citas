from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Base de datos
    database_url: str = "sqlite:///./reserva.db"
    
    # Seguridad JWT
    jwt_secret: str = "CAMBIA_ESTE_SECRETO_EN_PRODUCCION"
    access_token_expire_minutes: int = 60
    
    # CORS - se parsea desde string separado por comas
    cors_origins_str: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000"
    
    # Entorno
    environment: str = "development"
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        origins_str = os.getenv("CORS_ORIGINS", self.cors_origins_str)
        return [origin.strip() for origin in origins_str.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignorar campos extra en variables de entorno


settings = Settings()
