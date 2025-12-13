"""
Tests unitarios para utilidades de instalaciones
"""
import pytest
from app.utils.facilities import (
    create_facility,
    get_facility,
    list_facilities,
    update_facility,
    delete_facility
)


class TestFacilityUtils:
    """Tests para funciones de utilidad de instalaciones"""
    
    def test_create_facility(self, db_session):
        """Test creación de instalación"""
        facility = create_facility(
            db_session,
            nombre="Pista de Baloncesto",
            tipo="Baloncesto",
            aforo=10,
            activo=True
        )
        
        assert facility.id is not None
        assert facility.nombre == "Pista de Baloncesto"
        assert facility.tipo == "Baloncesto"
        assert facility.aforo == 10
        assert facility.activo is True
    
    def test_create_facility_default_active(self, db_session):
        """Test creación con activo por defecto"""
        facility = create_facility(
            db_session,
            nombre="Test",
            tipo=None,
            aforo=None
        )
        assert facility.activo is True
    
    def test_get_facility_exists(self, db_session, sample_facility):
        """Test obtener instalación existente"""
        facility = get_facility(db_session, sample_facility.id)
        
        assert facility is not None
        assert facility.id == sample_facility.id
        assert facility.nombre == sample_facility.nombre
    
    def test_get_facility_not_exists(self, db_session):
        """Test obtener instalación inexistente"""
        facility = get_facility(db_session, 99999)
        assert facility is None
    
    def test_list_facilities_all(self, db_session):
        """Test listar todas las instalaciones"""
        create_facility(db_session, nombre="Activa", tipo="Test", aforo=1, activo=True)
        create_facility(db_session, nombre="Inactiva", tipo="Test", aforo=1, activo=False)
        
        facilities = list_facilities(db_session, only_active=False)
        assert len(facilities) >= 2
    
    def test_list_facilities_only_active(self, db_session):
        """Test listar solo instalaciones activas"""
        create_facility(db_session, nombre="Activa", tipo="Test", aforo=1, activo=True)
        create_facility(db_session, nombre="Inactiva", tipo="Test", aforo=1, activo=False)
        
        facilities = list_facilities(db_session, only_active=True)
        assert all(f.activo for f in facilities)
    
    def test_update_facility(self, db_session, sample_facility):
        """Test actualización de instalación"""
        updated = update_facility(
            db_session,
            sample_facility,
            nombre="Nombre Actualizado",
            aforo=50
        )
        
        assert updated.nombre == "Nombre Actualizado"
        assert updated.aforo == 50
        assert updated.id == sample_facility.id
    
    def test_update_facility_partial(self, db_session, sample_facility):
        """Test actualización parcial"""
        original_nombre = sample_facility.nombre
        updated = update_facility(
            db_session,
            sample_facility,
            aforo=30
        )
        
        assert updated.nombre == original_nombre
        assert updated.aforo == 30
    
    def test_update_facility_none_values(self, db_session, sample_facility):
        """Test que valores None no se actualizan"""
        original_tipo = sample_facility.tipo
        updated = update_facility(
            db_session,
            sample_facility,
            tipo=None
        )
        # Si el valor es None, no debería cambiar
        assert updated.tipo == original_tipo
    
    def test_delete_facility(self, db_session, sample_facility):
        """Test eliminación de instalación"""
        fac_id = sample_facility.id
        delete_facility(db_session, sample_facility)
        
        assert get_facility(db_session, fac_id) is None

