from sqlalchemy import Integer, Date, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Slot(Base):
    __tablename__ = "franjas_horarias"
    __table_args__ = (UniqueConstraint("instalacion_id","fecha","hora_inicio","hora_fin", name="uq_slot"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    instalacion_id: Mapped[int] = mapped_column(ForeignKey("instalaciones.id"), nullable=False, index=True)
    fecha: Mapped[object] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[object] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[object] = mapped_column(Time, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    plazas_disponibles: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
