from pydantic import BaseModel, Field

class FacilityBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    tipo: str | None = Field(default=None, max_length=80)
    aforo: int | None = Field(default=None, ge=1)
    activo: bool = True

class FacilityCreate(FacilityBase):
    pass

class FacilityUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    tipo: str | None = Field(default=None, max_length=80)
    aforo: int | None = Field(default=None, ge=1)
    activo: bool | None = None

class FacilityOut(FacilityBase):
    id: int
    class Config:
        from_attributes = True
