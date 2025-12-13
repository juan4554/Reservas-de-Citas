"""Script simple para resetear la contraseña del admin"""
# Importar todos los modelos primero
from app.db.base import Base, User, Facility, Slot, Reservation
from app.db.session import SessionLocal
from app.core.security import hash_password

import sys

if len(sys.argv) < 2:
    print("Uso: python reset_admin.py <nueva_contrasena>")
    print("Ejemplo: python reset_admin.py admin123")
    sys.exit(1)

new_password = sys.argv[1]
db = SessionLocal()

try:
    admin = db.query(User).filter(User.email == "admin@test.local.es").first()
    
    if not admin:
        print("[ERROR] No se encontro el usuario admin")
        sys.exit(1)
    
    admin.hashed_password = hash_password(new_password)
    db.commit()
    
    print(f"[OK] Contrasena del admin reseteada exitosamente")
    print(f"     Email: {admin.email}")
    print(f"     Nueva contrasena: {new_password}")
    
except Exception as e:
    print(f"[ERROR] Error al resetear contrasena: {e}")
    db.rollback()
finally:
    db.close()

