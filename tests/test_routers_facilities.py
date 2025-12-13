"""
Tests unitarios para endpoints de instalaciones
"""
import pytest


class TestFacilitiesRouter:
    """Tests para el router de instalaciones"""
    
    def test_list_facilities(self, client, sample_facility):
        """Test listar instalaciones"""
        response = client.get("/facilities")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(f["id"] == sample_facility.id for f in data)
    
    def test_list_facilities_only_active(self, client, db_session):
        """Test listar solo instalaciones activas"""
        from app.utils.facilities import create_facility
        create_facility(db_session, nombre="Activa", tipo="Test", aforo=1, activo=True)
        create_facility(db_session, nombre="Inactiva", tipo="Test", aforo=1, activo=False)
        
        response = client.get("/facilities?only_active=true")
        
        assert response.status_code == 200
        data = response.json()
        assert all(f["activo"] for f in data)
    
    def test_get_facility(self, client, sample_facility):
        """Test obtener instalación específica"""
        response = client.get(f"/facilities/{sample_facility.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_facility.id
        assert data["nombre"] == sample_facility.nombre
    
    def test_get_facility_not_found(self, client):
        """Test obtener instalación inexistente"""
        response = client.get("/facilities/99999")
        
        assert response.status_code == 404
    
    def test_create_facility_admin(self, client, admin_headers):
        """Test crear instalación como admin"""
        response = client.post(
            "/facilities",
            json={
                "nombre": "Nueva Instalación",
                "tipo": "Test",
                "aforo": 10,
                "activo": True
            },
            headers=admin_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Nueva Instalación"
        assert data["tipo"] == "Test"
        assert data["aforo"] == 10
    
    def test_create_facility_non_admin(self, client, auth_headers):
        """Test que no admin no puede crear instalación"""
        response = client.post(
            "/facilities",
            json={
                "nombre": "Nueva Instalación",
                "tipo": "Test",
                "aforo": 10
            },
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_update_facility_admin(self, client, admin_headers, sample_facility):
        """Test actualizar instalación como admin"""
        response = client.patch(
            f"/facilities/{sample_facility.id}",
            json={
                "nombre": "Nombre Actualizado",
                "aforo": 50
            },
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Nombre Actualizado"
        assert data["aforo"] == 50
    
    def test_delete_facility_admin(self, client, admin_headers, sample_facility, db_session):
        """Test eliminar instalación como admin"""
        fac_id = sample_facility.id
        response = client.delete(
            f"/facilities/{fac_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 204
        
        # Verificar que fue eliminada
        get_response = client.get(f"/facilities/{fac_id}")
        assert get_response.status_code == 404

