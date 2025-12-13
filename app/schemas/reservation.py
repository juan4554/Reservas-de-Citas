from pydantic import BaseModel
from datetime import date, time

class ReservationCreate(BaseModel):
    instalacion_id: int
    franja_id: int

class ReservationOut(BaseModel):
    id: int
    usuario_id: int
    instalacion_id: int
    franja_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time

    class Config:
        from_attributes = True

class AdminReservationOut(BaseModel):
    id: int
    usuario_id: int
    usuario_nombre: str
    usuario_email: str
    instalacion_id: int
    instalacion_nombre: str
    franja_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        from_attributes = True