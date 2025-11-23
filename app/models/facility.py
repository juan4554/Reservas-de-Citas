from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Facility(Base):
    __tablename__ = "instalaciones"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(80))
    aforo: Mapped[int | None] = mapped_column(Integer)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    franjas = relationship("Slot", back_populates="instalacion", cascade="all, delete-orphan")
    reservas = relationship("Reservation", back_populates="instalacion", cascade="all, delete-orphan")
