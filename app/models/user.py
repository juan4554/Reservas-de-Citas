import enum
from sqlalchemy import String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class UserRole(str, enum.Enum):
    admin = "admin"
    cliente = "cliente"

class User(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.cliente, nullable=False)
    reservas = relationship("Reservation", back_populates="usuario", cascade="all, delete-orphan")
