"""
Configuración global de pytest con fixtures compartidas
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from datetime import date, time, datetime, timedelta
from faker import Faker

from app.db.base_class import Base
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User, UserRole
from app.models.facility import Facility
from app.models.slot import Slot
from app.models.reservation import Reservation
from app.core.security import hash_password

fake = Faker()

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea una sesión de base de datos para cada test"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        # Limpiar tablas después del test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de test para FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    from app.api.deps import get_db
    # Limpiar cualquier override previo
    app.dependency_overrides.clear()
    # Establecer el nuevo override
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar después del test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db_session: Session) -> User:
    """Usuario de prueba"""
    user = User(
        nombre="Test User",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        rol=UserRole.cliente
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session: Session) -> User:
    """Usuario administrador de prueba"""
    user = User(
        nombre="Admin User",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        rol=UserRole.admin
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_facility(db_session: Session) -> Facility:
    """Instalación de prueba"""
    facility = Facility(
        nombre="Pista de Tenis 1",
        tipo="Tenis",
        aforo=4,
        activo=True
    )
    db_session.add(facility)
    db_session.commit()
    db_session.refresh(facility)
    return facility


@pytest.fixture
def sample_slot(db_session: Session, sample_facility: Facility) -> Slot:
    """Franja horaria de prueba"""
    slot = Slot(
        instalacion_id=sample_facility.id,
        fecha=date.today() + timedelta(days=1),
        hora_inicio=time(10, 0),
        hora_fin=time(11, 0),
        capacidad=4,
        plazas_disponibles=4
    )
    db_session.add(slot)
    db_session.commit()
    db_session.refresh(slot)
    return slot


@pytest.fixture
def sample_reservation(db_session: Session, sample_user: User, sample_facility: Facility, sample_slot: Slot) -> Reservation:
    """Reserva de prueba"""
    reservation = Reservation(
        usuario_id=sample_user.id,
        instalacion_id=sample_facility.id,
        franja_id=sample_slot.id,
        estado="activa"
    )
    db_session.add(reservation)
    sample_slot.plazas_disponibles -= 1
    db_session.add(sample_slot)
    db_session.commit()
    db_session.refresh(reservation)
    return reservation


@pytest.fixture
def auth_headers(client, sample_user):
    """Headers de autenticación para requests"""
    response = client.post(
        "/auth/login",
        data={"username": sample_user.email, "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, admin_user):
    """Headers de autenticación para admin"""
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": "admin123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

