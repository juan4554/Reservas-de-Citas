"""
Tests unitarios para endpoints de reservas
"""
import pytest
from datetime import date, time, timedelta


class TestReservationsRouter:
    """Tests para el router de reservas"""
    
    def test_create_reservation(self, client, auth_headers, sample_facility, sample_slot, db_session):
        """Test crear reserva"""
        response = client.post(
            "/reservations",
            json={
                "instalacion_id": sample_facility.id,
                "franja_id": sample_slot.id
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["instalacion_id"] == sample_facility.id
        assert data["franja_id"] == sample_slot.id
        assert "id" in data
        assert "fecha" in data
        assert "hora_inicio" in data
        assert "hora_fin" in data
    
    def test_create_reservation_unauthorized(self, client, sample_facility, sample_slot):
        """Test crear reserva sin autenticación"""
        response = client.post(
            "/reservations",
            json={
                "instalacion_id": sample_facility.id,
                "franja_id": sample_slot.id
            }
        )
        
        assert response.status_code == 403
    
    def test_create_reservation_no_plazas(self, client, auth_headers, sample_facility, db_session):
        """Test crear reserva sin plazas disponibles"""
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
        
        response = client.post(
            "/reservations",
            json={
                "instalacion_id": sample_facility.id,
                "franja_id": slot.id
            },
            headers=auth_headers
        )
        
        assert response.status_code == 409
    
    def test_list_my_reservations(self, client, auth_headers, sample_reservation):
        """Test listar mis reservas"""
        response = client.get("/reservations/my", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(r["id"] == sample_reservation.id for r in data)
    
    def test_list_my_reservations_unauthorized(self, client):
        """Test listar reservas sin autenticación"""
        response = client.get("/reservations/my")
        
        assert response.status_code == 403
    
    def test_cancel_reservation(self, client, auth_headers, sample_user, sample_facility, sample_slot, db_session):
        """Test cancelar reserva"""
        from app.utils.reservations import create_reservation
        reservation = create_reservation(
            db_session,
            user=sample_user,
            instalacion_id=sample_facility.id,
            franja_id=sample_slot.id
        )
        
        response = client.delete(
            f"/reservations/{reservation.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
    
    def test_cancel_reservation_not_found(self, client, auth_headers):
        """Test cancelar reserva inexistente"""
        response = client.delete(
            "/reservations/99999",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_cancel_reservation_unauthorized(self, client, sample_reservation):
        """Test cancelar reserva sin autenticación"""
        response = client.delete(f"/reservations/{sample_reservation.id}")
        
        assert response.status_code == 403

