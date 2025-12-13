# app/api/routers/admin_reservations.py
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.utils.admin_reservations import list_reservations, admin_cancel_reservation
from app.schemas.reservation import AdminReservationOut
from app.models.slot import Slot

router = APIRouter(prefix="/admin/reservations", tags=["admin-reservations"], dependencies=[Depends(require_admin)])


@router.get("", response_model=dict)
def admin_list_reservations(
    usuario_id: Optional[int] = Query(default=None),
    instalacion_id: Optional[int] = Query(default=None),
    fecha: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    estado: Optional[str] = Query(default=None, description="activa|cancelada"),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = list_reservations(
        db,
        usuario_id=usuario_id,
        instalacion_id=instalacion_id,
        fecha=fecha,
        estado=estado,
        limit=limit,
        offset=offset,
    )
    
    # Serializar con datos completos
    result = []
    for res in items:
        slot = res.franja
        result.append({
            "id": res.id,
            "usuario_id": res.usuario_id,
            "usuario_nombre": res.usuario.nombre,
            "usuario_email": res.usuario.email,
            "instalacion_id": res.instalacion_id,
            "instalacion_nombre": res.instalacion.nombre,
            "franja_id": res.franja_id,
            "fecha": slot.fecha,
            "hora_inicio": slot.hora_inicio,
            "hora_fin": slot.hora_fin,
            "estado": res.estado,
        })
    
    return {"total": total, "limit": limit, "offset": offset, "items": result}


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_reservation(reserva_id: int, db: Session = Depends(get_db)):
    admin_cancel_reservation(db, reserva_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
