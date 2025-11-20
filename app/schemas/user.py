from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    cliente = "cliente"

class UserRegister(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: UserRole
    class Config:
        from_attributes = True  
        # para devolver objetos ORM

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
