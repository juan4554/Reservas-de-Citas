from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.utils.reservations import (
    create_reservation, list_reservations_for_user, get_reservation, cancel_reservation
)
from app.models.user import User
from app.models.slot import Slot

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def book(data: ReservationCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    res = create_reservation(db, user=current, instalacion_id=data.instalacion_id, franja_id=data.franja_id)
    slot = db.get(Slot, res.franja_id)  # completar fecha/hora en respuesta
    return {
        "id": res.id,
        "usuario_id": res.usuario_id,
        "instalacion_id": res.instalacion_id,
        "franja_id": res.franja_id,
        "fecha": slot.fecha,
        "hora_inicio": slot.hora_inicio,
        "hora_fin": slot.hora_fin,
    }

@router.get("/my", response_model=list[ReservationOut])
def my_reservations(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    reservas = list_reservations_for_user(db, current.id)
    out = []
    for r in reservas:
        slot = db.get(Slot, r.franja_id)
        out.append({
            "id": r.id,
            "usuario_id": r.usuario_id,
            "instalacion_id": r.instalacion_id,
            "franja_id": r.franja_id,
            "fecha": slot.fecha,
            "hora_inicio": slot.hora_inicio,
            "hora_fin": slot.hora_fin,
        })
    return out

@router.delete("/{res_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel(res_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    res = get_reservation(db, res_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    cancel_reservation(db, res=res, user=current)
    return None
