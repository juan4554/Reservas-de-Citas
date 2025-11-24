# app/api/routers/admin_users.py
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_db, require_admin
from app.models.user import User
from app.utils.admin_users import list_users, set_role, set_active

router = APIRouter(prefix="/admin/users", tags=["admin-users"], dependencies=[Depends(require_admin)])


class RoleUpdate(BaseModel):
    rol: str  # "admin" | "cliente"


class StatusUpdate(BaseModel):
    activo: bool


@router.get("")
def admin_list_users(
    q: Optional[str] = Query(default=None, description="Búsqueda por email/nombre"),
    rol: Optional[str] = Query(default=None, description="admin|cliente"),
    activo: Optional[bool] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = list_users(db, q=q, rol=rol, activo=activo, limit=limit, offset=offset)
    return {"total": total, "limit": limit, "offset": offset, "items": items}


@router.get("/{user_id}")
def admin_get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}/role")
def admin_update_role(user_id: int, body: RoleUpdate, db: Session = Depends(get_db)):
    user = set_role(db, user_id, body.rol)
    return user


@router.patch("/{user_id}/status")
def admin_update_status(user_id: int, body: StatusUpdate, db: Session = Depends(get_db)):
    user = set_active(db, user_id, body.activo)
    return user
