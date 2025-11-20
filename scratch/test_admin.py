import sys, pathlib
sys.path.append(str(pathlib.Path(".").resolve()))
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.users import create_user
from app.models.user import UserRole

db: Session = SessionLocal()
try:
    u = create_user(db, nombre="Admin", email="admin@test.local.es", password="Admin1234", rol=UserRole.admin)
    print("Admin creado:", u.email, u.id)
except Exception as e:
    print("Posible ya existe:", e)
finally:
    db.close()
