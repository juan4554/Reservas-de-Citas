from sqlalchemy import Column, Integer, ForeignKey, String  # <-- añade String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Reservation(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    instalacion_id = Column(Integer, ForeignKey("instalaciones.id", ondelete="CASCADE"), nullable=False, index=True)
    franja_id = Column(Integer, ForeignKey("franjas_horarias.id", ondelete="CASCADE"), nullable=False, index=True)

    # NUEVO: alineado con tu BD
    #estado = Column(String(20), nullable=False, server_default="activa")
    estado = Column(String(20), nullable=False, default="activa")
    usuario = relationship("User", back_populates="reservas")
    instalacion = relationship("Facility", back_populates="reservas")
    franja = relationship("Slot", back_populates="reservas")
