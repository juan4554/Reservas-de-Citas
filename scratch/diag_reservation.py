import sys, pathlib
sys.path.append(str(pathlib.Path(".").resolve()))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.slot import Slot
from app.utils.reservations import create_reservation

db: Session = SessionLocal()
try:
    # ajusta estos IDs si hace falta
    user = db.query(User).first()
    slot = db.get(Slot, 1)
    print("User:", user.id if user else None, "Slot:", slot.id if slot else None, "Instalación slot:", getattr(slot, "instalacion_id", None))
    if not user or not slot:
        print("Faltan datos: crea usuario o franja primero")
        raise SystemExit(0)

    res = create_reservation(db, user=user, instalacion_id=slot.instalacion_id, franja_id=slot.id)
    print("Reserva creada OK:", res.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
