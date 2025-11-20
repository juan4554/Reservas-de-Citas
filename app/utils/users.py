from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, nombre: str, email: str, password: str, rol: UserRole = UserRole.cliente) -> User:
    user = User(nombre=nombre, email=email, hashed_password=hash_password(password), rol=rol)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
