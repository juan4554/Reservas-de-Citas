"""
Tests unitarios para endpoints de franjas horarias
"""
import pytest
from datetime import date, time, timedelta


class TestSlotsRouter:
    """Tests para el router de franjas horarias"""
    
    def test_create_slot_admin(self, client, admin_headers, sample_facility):
        """Test crear franja como admin"""
        test_date = date.today() + timedelta(days=1)
        response = client.post(
            "/slots",
            json={
                "instalacion_id": sample_facility.id,
                "fecha": test_date.isoformat(),
                "hora_inicio": "10:00:00",
                "hora_fin": "11:00:00",
                "capacidad": 4,
                "plazas_disponibles": 4
            },
            headers=admin_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["instalacion_id"] == sample_facility.id
        assert data["capacidad"] == 4
        assert data["plazas_disponibles"] == 4
    
    def test_create_slot_non_admin(self, client, auth_headers, sample_facility):
        """Test que no admin no puede crear franja"""
        test_date = date.today() + timedelta(days=1)
        response = client.post(
            "/slots",
            json={
                "instalacion_id": sample_facility.id,
                "fecha": test_date.isoformat(),
                "hora_inicio": "10:00:00",
                "hora_fin": "11:00:00",
                "capacidad": 4
            },
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_create_slot_invalid_time(self, client, admin_headers, sample_facility):
        """Test crear franja con hora_fin anterior a hora_inicio"""
        test_date = date.today() + timedelta(days=1)
        response = client.post(
            "/slots",
            json={
                "instalacion_id": sample_facility.id,
                "fecha": test_date.isoformat(),
                "hora_inicio": "11:00:00",
                "hora_fin": "10:00:00",  # Antes de inicio
                "capacidad": 4
            },
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_list_slots_by_facility(self, client, sample_facility, sample_slot):
        """Test listar franjas por instalación y fecha"""
        response = client.get(
            f"/slots/by-facility/{sample_facility.id}",
            params={"fecha": sample_slot.fecha.isoformat()}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(s["id"] == sample_slot.id for s in data)
    
    def test_list_slots_only_available(self, client, sample_facility, db_session):
        """Test listar solo franjas disponibles"""
        from app.models.slot import Slot
        test_date = date.today() + timedelta(days=1)
        
        slot1 = Slot(
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4,
            plazas_disponibles=4
        )
        slot2 = Slot(
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(11, 0),
            hora_fin=time(12, 0),
            capacidad=4,
            plazas_disponibles=0
        )
        db_session.add(slot1)
        db_session.add(slot2)
        db_session.commit()
        
        response = client.get(
            f"/slots/by-facility/{sample_facility.id}",
            params={
                "fecha": test_date.isoformat(),
                "available_only": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(s["plazas_disponibles"] > 0 for s in data)
    
    def test_delete_slot_admin(self, client, admin_headers, sample_slot):
        """Test eliminar franja como admin"""
        slot_id = sample_slot.id
        response = client.delete(
            f"/slots/{slot_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 204
        
        # Verificar que fue eliminada
        get_response = client.get(
            f"/slots/by-facility/{sample_slot.instalacion_id}",
            params={"fecha": sample_slot.fecha.isoformat()}
        )
        data = get_response.json()
        assert not any(s["id"] == slot_id for s in data)

