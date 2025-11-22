from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from datetime import date
from app.models.slot import Slot

def create_slot(db: Session, *, instalacion_id: int, fecha, hora_inicio, hora_fin, capacidad: int, plazas_disponibles: int | None = None) -> Slot:
    slot = Slot(
        instalacion_id=instalacion_id,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        capacidad=capacidad,
        plazas_disponibles=plazas_disponibles if plazas_disponibles is not None else capacidad,
    )
    db.add(slot)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Ya existe una franja idéntica para esa instalación y horario") from e
    db.refresh(slot)
    return slot

def list_slots_for_facility_date(db: Session, *, instalacion_id: int, fecha: date, only_available: bool = False) -> list[Slot]:
    stmt = select(Slot).where(and_(Slot.instalacion_id == instalacion_id, Slot.fecha == fecha))
    if only_available:
        stmt = stmt.where(Slot.plazas_disponibles > 0)
    return list(db.scalars(stmt).all())

def delete_slot(db: Session, slot: Slot) -> None:
    db.delete(slot)
    db.commit()

def get_slot(db: Session, slot_id: int) -> Slot | None:
    return db.get(Slot, slot_id)
