# app/utils/admin_reservations.py
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status

from app.models.reservation import Reservation
from app.models.slot import Slot
from app.models.user import User
from app.models.facility import Facility

def list_reservations(
    db: Session,
    usuario_id: Optional[int] = None,
    instalacion_id: Optional[int] = None,
    fecha: Optional[str] = None,  # "YYYY-MM-DD"
    estado: Optional[str] = None,  # "activa" | "cancelada"
    limit: int = 20,
    offset: int = 0,
) -> Tuple[List[Reservation], int]:
    limit = max(1, min(100, limit))
    offset = max(0, offset)

    q = db.query(Reservation).options(
        joinedload(Reservation.franja),
        joinedload(Reservation.usuario),
        joinedload(Reservation.instalacion)
    )

    if usuario_id:
        q = q.filter(Reservation.usuario_id == usuario_id)

    if instalacion_id:
        q = q.filter(Reservation.instalacion_id == instalacion_id)

    if estado:
        q = q.filter(Reservation.estado == estado)

    if fecha:
        # Join por Slot.fecha
        q = q.join(Slot, Reservation.franja_id == Slot.id).filter(Slot.fecha == fecha)

    total = q.count()
    items = q.order_by(Reservation.id.desc()).limit(limit).offset(offset).all()
    return items, total


def admin_cancel_reservation(db: Session, reserva_id: int) -> None:
    res = db.get(Reservation, reserva_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

    if res.estado == "cancelada":
        # Idempotente: no hacemos nada, pero no es error
        return

    # Recuperar plaza en la franja
    slot = db.get(Slot, res.franja_id)
    if slot:
        slot.plazas_disponibles = max(0, slot.plazas_disponibles + 1)
        db.add(slot)

    res.estado = "cancelada"
    db.add(res)
    db.commit()
