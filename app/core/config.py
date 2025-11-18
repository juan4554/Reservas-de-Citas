import os
from pydantic import BaseModel

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./reserva.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "CAMBIA_ESTE_SECRETO")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
settings = Settings()
