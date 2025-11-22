from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.facility import Facility

def create_facility(db: Session, *, nombre: str, tipo: str | None, aforo: int | None, activo: bool = True) -> Facility:
    fac = Facility(nombre=nombre, tipo=tipo, aforo=aforo, activo=activo)
    db.add(fac)
    db.commit()
    db.refresh(fac)
    return fac

def get_facility(db: Session, fac_id: int) -> Facility | None:
    return db.get(Facility, fac_id)

def list_facilities(db: Session, only_active: bool = True) -> list[Facility]:
    stmt = select(Facility)
    if only_active:
        stmt = stmt.where(Facility.activo.is_(True))
    return list(db.scalars(stmt).all())

def update_facility(db: Session, fac: Facility, **changes) -> Facility:
    for k, v in changes.items():
        if v is not None:
            setattr(fac, k, v)
    db.add(fac)
    db.commit()
    db.refresh(fac)
    return fac

def delete_facility(db: Session, fac: Facility) -> None:
    db.delete(fac)
    db.commit()
