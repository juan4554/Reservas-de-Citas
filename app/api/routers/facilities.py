from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin
from app.schemas.facility import FacilityCreate, FacilityUpdate, FacilityOut
from app.utils.facilities import create_facility, get_facility, list_facilities, update_facility, delete_facility
from app.models.user import User

router = APIRouter(prefix="/facilities", tags=["Facilities"])

@router.get("", response_model=list[FacilityOut])
def list_all(only_active: bool = Query(True), db: Session = Depends(get_db)):
    return list_facilities(db, only_active=only_active)

@router.get("/{fac_id}", response_model=FacilityOut)
def retrieve(fac_id: int, db: Session = Depends(get_db)):
    fac = get_facility(db, fac_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    return fac

@router.post("", response_model=FacilityOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create(data: FacilityCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return create_facility(db, nombre=data.nombre, tipo=data.tipo, aforo=data.aforo, activo=data.activo)

@router.patch("/{fac_id}", response_model=FacilityOut, dependencies=[Depends(require_admin)])
def patch(fac_id: int, data: FacilityUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    fac = get_facility(db, fac_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    return update_facility(db, fac, **data.model_dump(exclude_unset=True))

@router.delete("/{fac_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def remove(fac_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    fac = get_facility(db, fac_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    delete_facility(db, fac)
    return None
