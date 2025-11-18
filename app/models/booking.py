import enum
from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class BookingStatus(str, enum.Enum):
    activa = "activa"
    cancelada = "cancelada"

class Booking(Base):
    __tablename__ = "reservas"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    instalacion_id: Mapped[int] = mapped_column(ForeignKey("instalaciones.id"), nullable=False, index=True)
    franja_id: Mapped[int] = mapped_column(ForeignKey("franjas_horarias.id"), nullable=False, index=True)
    estado: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.activa, nullable=False)
