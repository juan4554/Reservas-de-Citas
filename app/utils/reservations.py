from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from app.models.reservation import Reservation
from app.models.slot import Slot
from app.models.user import User
from datetime import date

def _get_slot_for_update(db: Session, franja_id: int) -> Slot | None:
    # En SQLite no hay FOR UPDATE; en Postgres podríamos bloquear fila.
    return db.get(Slot, franja_id)

def _user_has_overlap(db: Session, user_id: int, fecha: date, hora_inicio, hora_fin) -> bool:
    stmt = (
        select(Reservation)
        .where(Reservation.usuario_id == user_id)
        .join(Slot, Slot.id == Reservation.franja_id)
        .where(Slot.fecha == fecha)
        .where(and_(Slot.hora_inicio < hora_fin, hora_inicio < Slot.hora_fin))
    )
    return db.scalars(stmt).first() is not None

def create_reservation(db: Session, *, user: User, instalacion_id: int, franja_id: int) -> Reservation:
    slot = _get_slot_for_update(db, franja_id)
    if not slot or slot.instalacion_id != instalacion_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Franja inexistente para esa instalación")

    if slot.plazas_disponibles <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No quedan plazas en esta franja")

    if _user_has_overlap(db, user.id, slot.fecha, slot.hora_inicio, slot.hora_fin):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya tienes una reserva solapada en ese horario")

    res = Reservation(usuario_id=user.id, instalacion_id=instalacion_id, franja_id=franja_id)
    db.add(res)
    slot.plazas_disponibles -= 1
    db.add(slot)
    db.commit()
    db.refresh(res)
    return res

def list_reservations_for_user(db: Session, user_id: int) -> list[Reservation]:
    stmt = select(Reservation).where(Reservation.usuario_id == user_id).order_by(Reservation.id.desc())
    return list(db.scalars(stmt).all())

def get_reservation(db: Session, res_id: int) -> Reservation | None:
    return db.get(Reservation, res_id)

def cancel_reservation(db: Session, *, res: Reservation, user: User) -> None:
    if res.usuario_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes cancelar reservas de otros usuarios")

    slot = db.get(Slot, res.franja_id)
    if slot:
        slot.plazas_disponibles += 1
        db.add(slot)
    db.delete(res)
    db.commit()
