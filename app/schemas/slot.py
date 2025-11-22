from pydantic import BaseModel, Field, field_validator
from datetime import date, time

class SlotBase(BaseModel):
    instalacion_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    capacidad: int = Field(ge=1)
    plazas_disponibles: int | None = None  # si None → se iguala a capacidad

    @field_validator("hora_fin")
    @classmethod
    def _fin_posterior(cls, v, info):
        ini = info.data.get("hora_inicio")
        if ini and v <= ini:
            raise ValueError("hora_fin debe ser posterior a hora_inicio")
        return v

    @field_validator("plazas_disponibles")
    @classmethod
    def _plazas_no_superan_cap(cls, v, info):
        cap = info.data.get("capacidad")
        if v is None:
            return cap
        if cap is not None and v > cap:
            raise ValueError("plazas_disponibles no puede superar capacidad")
        return v

class SlotCreate(SlotBase):
    pass

class SlotOut(BaseModel):
    id: int
    instalacion_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    capacidad: int
    plazas_disponibles: int
    class Config:
        from_attributes = True
