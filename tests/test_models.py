"""
Tests unitarios para modelos de la base de datos
"""
import pytest
from datetime import date, time
from sqlalchemy.exc import IntegrityError

from app.models.user import User, UserRole
from app.models.facility import Facility
from app.models.slot import Slot
from app.models.reservation import Reservation
from app.core.security import hash_password


class TestUserModel:
    """Tests para el modelo User"""
    
    def test_create_user(self, db_session):
        """Test creación de usuario"""
        user = User(
            nombre="Juan Pérez",
            email="juan@example.com",
            hashed_password=hash_password("password123"),
            rol=UserRole.cliente
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.nombre == "Juan Pérez"
        assert user.email == "juan@example.com"
        assert user.rol == UserRole.cliente
    
    def test_user_email_unique(self, db_session, sample_user):
        """Test que el email debe ser único"""
        duplicate = User(
            nombre="Otro Usuario",
            email=sample_user.email,
            hashed_password=hash_password("password"),
            rol=UserRole.cliente
        )
        db_session.add(duplicate)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_default_role(self, db_session):
        """Test que el rol por defecto es cliente"""
        user = User(
            nombre="Test",
            email="test@example.com",
            hashed_password=hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        assert user.rol == UserRole.cliente


class TestFacilityModel:
    """Tests para el modelo Facility"""
    
    def test_create_facility(self, db_session):
        """Test creación de instalación"""
        facility = Facility(
            nombre="Pista de Fútbol",
            tipo="Fútbol",
            aforo=22,
            activo=True
        )
        db_session.add(facility)
        db_session.commit()
        
        assert facility.id is not None
        assert facility.nombre == "Pista de Fútbol"
        assert facility.tipo == "Fútbol"
        assert facility.aforo == 22
        assert facility.activo is True
    
    def test_facility_default_active(self, db_session):
        """Test que activo por defecto es True"""
        facility = Facility(nombre="Test", tipo="Test")
        db_session.add(facility)
        db_session.commit()
        assert facility.activo is True


class TestSlotModel:
    """Tests para el modelo Slot"""
    
    def test_create_slot(self, db_session, sample_facility):
        """Test creación de franja horaria"""
        slot = Slot(
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4,
            plazas_disponibles=4
        )
        db_session.add(slot)
        db_session.commit()
        
        assert slot.id is not None
        assert slot.instalacion_id == sample_facility.id
        assert slot.capacidad == 4
        assert slot.plazas_disponibles == 4
    
    def test_slot_default_capacity(self, db_session, sample_facility):
        """Test valores por defecto de capacidad"""
        slot = Slot(
            instalacion_id=sample_facility.id,
            fecha=date.today(),
            hora_inicio=time(9, 0),
            hora_fin=time(10, 0)
        )
        db_session.add(slot)
        db_session.commit()
        assert slot.capacidad == 1
        assert slot.plazas_disponibles == 1
    
    def test_slot_unique_constraint(self, db_session, sample_facility):
        """Test constraint único de slot"""
        slot1 = Slot(
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4
        )
        db_session.add(slot1)
        db_session.commit()
        
        # Intentar crear slot duplicado
        slot2 = Slot(
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4
        )
        db_session.add(slot2)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestReservationModel:
    """Tests para el modelo Reservation"""
    
    def test_create_reservation(self, db_session, sample_user, sample_facility, sample_slot):
        """Test creación de reserva"""
        reservation = Reservation(
            usuario_id=sample_user.id,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id,
            estado="activa"
        )
        db_session.add(reservation)
        db_session.commit()
        
        assert reservation.id is not None
        assert reservation.usuario_id == sample_user.id
        assert reservation.instalacion_id == sample_facility.id
        assert reservation.franja_id == sample_slot.id
        assert reservation.estado == "activa"
    
    def test_reservation_default_state(self, db_session, sample_user, sample_facility, sample_slot):
        """Test estado por defecto de reserva"""
        reservation = Reservation(
            usuario_id=sample_user.id,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        db_session.add(reservation)
        db_session.commit()
        assert reservation.estado == "activa"
    
    def test_reservation_cascade_delete_user(self, db_session, sample_user, sample_facility, sample_slot):
        """Test que al eliminar usuario se eliminan sus reservas"""
        reservation = Reservation(
            usuario_id=sample_user.id,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        db_session.add(reservation)
        db_session.commit()
        res_id = reservation.id
        
        db_session.delete(sample_user)
        db_session.commit()
        
        assert db_session.get(Reservation, res_id) is None

