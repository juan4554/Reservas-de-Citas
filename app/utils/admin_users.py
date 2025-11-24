# app/utils/admin_users.py
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.user import User

def list_users(
    db: Session,
    q: Optional[str] = None,
    rol: Optional[str] = None,
    activo: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
) -> Tuple[List[User], int]:
    limit = max(1, min(100, limit))
    offset = max(0, offset)

    query = db.query(User)

    if q:
        qs = f"%{q.strip()}%"
        query = query.filter(or_(User.email.ilike(qs), User.nombre.ilike(qs))) if hasattr(User, "nombre") else query.filter(User.email.ilike(qs))

    if rol:
        if rol not in ("admin", "cliente"):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Rol inválido")
        query = query.filter(User.rol == rol)

    if activo is not None:
        query = query.filter(User.activo == bool(activo))

    total = query.count()
    items = query.order_by(User.id.desc()).limit(limit).offset(offset).all()
    return items, total


def _hay_otro_admin(db: Session, excluir_user_id: Optional[int] = None) -> bool:
    q = db.query(User).filter(User.rol == "admin", User.activo == True)  # noqa: E712
    if excluir_user_id:
        q = q.filter(User.id != excluir_user_id)
    return db.query(q.exists()).scalar()


def set_role(db: Session, user_id: int, new_role: str) -> User:
    if new_role not in ("admin", "cliente"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Rol inválido")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # No permitir dejar sin admins
    if user.rol == "admin" and new_role != "admin":
        if not _hay_otro_admin(db, excluir_user_id=user.id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No puedes dejar el sistema sin administradores")

    user.rol = new_role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def set_active(db: Session, user_id: int, active: bool) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # No permitir desactivar al último admin
    if user.rol == "admin" and active is False:
        if not _hay_otro_admin(db, excluir_user_id=user.id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No puedes desactivar al único admin")

    user.activo = bool(active)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
