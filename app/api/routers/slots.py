from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.api.deps import get_db, require_admin
from app.schemas.slot import SlotCreate, SlotOut
from app.utils.slots import create_slot, list_slots_for_facility_date, get_slot, delete_slot
from app.utils.facilities import get_facility
from app.models.user import User

router = APIRouter(prefix="/slots", tags=["Slots"])

@router.post("", response_model=SlotOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create(data: SlotCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    fac = get_facility(db, data.instalacion_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    try:
        return create_slot(
            db,
            instalacion_id=data.instalacion_id,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            capacidad=data.capacidad,
            plazas_disponibles=data.plazas_disponibles,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/by-facility/{fac_id}", response_model=list[SlotOut])
def list_for_facility(
    fac_id: int,
    fecha: date = Query(..., description="YYYY-MM-DD"),
    available_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    fac = get_facility(db, fac_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    return list_slots_for_facility_date(db, instalacion_id=fac_id, fecha=fecha, only_available=available_only)

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def remove(slot_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    slot = get_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Franja no encontrada")
    delete_slot(db, slot)
    return None
