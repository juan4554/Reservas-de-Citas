"""
Tests unitarios para utilidades de reservas
"""
import pytest
from datetime import date, time, timedelta
from fastapi import HTTPException

from app.utils.reservations import (
    create_reservation,
    list_reservations_for_user,
    get_reservation,
    cancel_reservation
)
from app.models.reservation import Reservation


class TestReservationUtils:
    """Tests para funciones de utilidad de reservas"""
    
    def test_create_reservation(self, db_session, sample_user, sample_facility, sample_slot):
        """Test creación de reserva"""
        initial_plazas = sample_slot.plazas_disponibles
        
        reservation = create_reservation(
            db_session,
            user=sample_user,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        
        assert reservation.id is not None
        assert reservation.usuario_id == sample_user.id
        assert reservation.instalacion_id == sample_facility.id
        assert reservation.franja_id == sample_slot.id
        
        # Verificar que se redujeron las plazas disponibles
        db_session.refresh(sample_slot)
        assert sample_slot.plazas_disponibles == initial_plazas - 1
    
    def test_create_reservation_no_plazas(self, db_session, sample_user, sample_facility):
        """Test que no se puede reservar si no hay plazas"""
        # Crear slot sin plazas
        from app.models.slot import Slot
        slot = Slot(
            instalacion_id=sample_facility.id,
            fecha=date.today() + timedelta(days=1),
            hora_inicio=time(14, 0),
            hora_fin=time(15, 0),
            capacidad=1,
            plazas_disponibles=0
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)
        
        with pytest.raises(HTTPException) as exc_info:
            create_reservation(
                db_session,
                user=sample_user,
                instalacion_id=sample_facility.id,
                franja_id=slot.id
            )
        assert exc_info.value.status_code == 409
    
    def test_create_reservation_slot_not_found(self, db_session, sample_user, sample_facility):
        """Test que no se puede reservar franja inexistente"""
        with pytest.raises(HTTPException) as exc_info:
            create_reservation(
                db_session,
                user=sample_user,
                instalacion_id=sample_facility.id,
                franja_id=99999
            )
        assert exc_info.value.status_code == 404
    
    def test_create_reservation_wrong_facility(self, db_session, sample_user, sample_facility, sample_slot):
        """Test que no se puede reservar franja de otra instalación"""
        # Crear otra instalación
        from app.models.facility import Facility
        other_facility = Facility(nombre="Otra", tipo="Test", activo=True)
        db_session.add(other_facility)
        db_session.commit()
        db_session.refresh(other_facility)
        
        with pytest.raises(HTTPException) as exc_info:
            create_reservation(
                db_session,
                user=sample_user,
                instalacion_id=other_facility.id,
                franja_id=sample_slot.id
            )
        assert exc_info.value.status_code == 404
    
    def test_create_reservation_overlap(self, db_session, sample_user, sample_facility):
        """Test que no se puede reservar con solapamiento"""
        fecha = date.today() + timedelta(days=1)
        
        # Crear primera reserva
        slot1 = db_session.query(type(sample_facility)).filter_by(id=sample_facility.id).first()
        from app.models.slot import Slot
        slot1_obj = Slot(
            instalacion_id=sample_facility.id,
            fecha=fecha,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4,
            plazas_disponibles=4
        )
        db_session.add(slot1_obj)
        db_session.commit()
        db_session.refresh(slot1_obj)
        
        reservation1 = create_reservation(
            db_session,
            user=sample_user,
            instalacion_id=sample_facility.id,
            franja_id=slot1_obj.id
        )
        
        # Intentar crear reserva solapada
        slot2 = Slot(
            instalacion_id=sample_facility.id,
            fecha=fecha,
            hora_inicio=time(10, 30),
            hora_fin=time(11, 30),
            capacidad=4,
            plazas_disponibles=4
        )
        db_session.add(slot2)
        db_session.commit()
        db_session.refresh(slot2)
        
        with pytest.raises(HTTPException) as exc_info:
            create_reservation(
                db_session,
                user=sample_user,
                instalacion_id=sample_facility.id,
                franja_id=slot2.id
            )
        assert exc_info.value.status_code == 409
    
    def test_list_reservations_for_user(self, db_session, sample_user, sample_reservation):
        """Test listar reservas de usuario"""
        reservations = list_reservations_for_user(db_session, sample_user.id)
        
        assert len(reservations) >= 1
        assert any(r.id == sample_reservation.id for r in reservations)
        assert all(r.usuario_id == sample_user.id for r in reservations)
    
    def test_get_reservation(self, db_session, sample_reservation):
        """Test obtener reserva"""
        reservation = get_reservation(db_session, sample_reservation.id)
        
        assert reservation is not None
        assert reservation.id == sample_reservation.id
    
    def test_get_reservation_not_exists(self, db_session):
        """Test obtener reserva inexistente"""
        reservation = get_reservation(db_session, 99999)
        assert reservation is None
    
    def test_cancel_reservation(self, db_session, sample_user, sample_facility, sample_slot):
        """Test cancelación de reserva"""
        reservation = create_reservation(
            db_session,
            user=sample_user,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        
        initial_plazas = sample_slot.plazas_disponibles
        db_session.refresh(sample_slot)
        plazas_after_reservation = sample_slot.plazas_disponibles
        
        cancel_reservation(db_session, res=reservation, user=sample_user)
        
        # Verificar que se liberaron las plazas
        db_session.refresh(sample_slot)
        assert sample_slot.plazas_disponibles == plazas_after_reservation + 1
        
        # Verificar que la reserva fue eliminada
        assert get_reservation(db_session, reservation.id) is None
    
    def test_cancel_reservation_other_user(self, db_session, sample_user, admin_user, sample_facility, sample_slot):
        """Test que no se puede cancelar reserva de otro usuario"""
        reservation = create_reservation(
            db_session,
            user=sample_user,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        
        with pytest.raises(HTTPException) as exc_info:
            cancel_reservation(db_session, res=reservation, user=admin_user)
        assert exc_info.value.status_code == 403

