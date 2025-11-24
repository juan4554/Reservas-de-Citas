# app/api/routers/admin_reservations.py
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.utils.admin_reservations import list_reservations, admin_cancel_reservation

router = APIRouter(prefix="/admin/reservations", tags=["admin-reservations"], dependencies=[Depends(require_admin)])


@router.get("")
def admin_list_reservations(
    usuario_id: Optional[int] = Query(default=None),
    instalacion_id: Optional[int] = Query(default=None),
    fecha: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    estado: Optional[str] = Query(default=None, description="activa|cancelada"),
    limit: int = Query(default=20, ge=1, le=100),
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
    return {"total": total, "limit": limit, "offset": offset, "items": items}


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_reservation(reserva_id: int, db: Session = Depends(get_db)):
    admin_cancel_reservation(db, reserva_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
