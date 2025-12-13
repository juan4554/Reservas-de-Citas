"""
Tests unitarios para utilidades de franjas horarias
"""
import pytest
from datetime import date, time
from sqlalchemy.exc import IntegrityError

from app.utils.slots import (
    create_slot,
    get_slot,
    list_slots_for_facility_date,
    delete_slot
)


class TestSlotUtils:
    """Tests para funciones de utilidad de franjas horarias"""
    
    def test_create_slot(self, db_session, sample_facility):
        """Test creación de franja horaria"""
        slot = create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4,
            plazas_disponibles=4
        )
        
        assert slot.id is not None
        assert slot.instalacion_id == sample_facility.id
        assert slot.capacidad == 4
        assert slot.plazas_disponibles == 4
    
    def test_create_slot_default_plazas(self, db_session, sample_facility):
        """Test que plazas_disponibles se iguala a capacidad si es None"""
        slot = create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=5,
            plazas_disponibles=None
        )
        
        assert slot.plazas_disponibles == 5
    
    def test_create_slot_duplicate_raises_error(self, db_session, sample_facility):
        """Test que crear slot duplicado lanza error"""
        create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=date(2024, 12, 25),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4
        )
        
        with pytest.raises(ValueError, match="Ya existe una franja"):
            create_slot(
                db_session,
                instalacion_id=sample_facility.id,
                fecha=date(2024, 12, 25),
                hora_inicio=time(10, 0),
                hora_fin=time(11, 0),
                capacidad=4
            )
    
    def test_get_slot_exists(self, db_session, sample_slot):
        """Test obtener franja existente"""
        slot = get_slot(db_session, sample_slot.id)
        
        assert slot is not None
        assert slot.id == sample_slot.id
    
    def test_get_slot_not_exists(self, db_session):
        """Test obtener franja inexistente"""
        slot = get_slot(db_session, 99999)
        assert slot is None
    
    def test_list_slots_for_facility_date(self, db_session, sample_facility):
        """Test listar franjas por instalación y fecha"""
        test_date = date(2024, 12, 25)
        create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4
        )
        create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(11, 0),
            hora_fin=time(12, 0),
            capacidad=4
        )
        
        slots = list_slots_for_facility_date(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date
        )
        
        assert len(slots) >= 2
        assert all(s.fecha == test_date for s in slots)
        assert all(s.instalacion_id == sample_facility.id for s in slots)
    
    def test_list_slots_only_available(self, db_session, sample_facility):
        """Test listar solo franjas disponibles"""
        test_date = date(2024, 12, 25)
        slot1 = create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            capacidad=4,
            plazas_disponibles=4
        )
        slot2 = create_slot(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date,
            hora_inicio=time(11, 0),
            hora_fin=time(12, 0),
            capacidad=4,
            plazas_disponibles=0
        )
        
        slots = list_slots_for_facility_date(
            db_session,
            instalacion_id=sample_facility.id,
            fecha=test_date,
            only_available=True
        )
        
        assert len(slots) >= 1
        assert all(s.plazas_disponibles > 0 for s in slots)
        assert slot1 in slots
        assert slot2 not in slots
    
    def test_delete_slot(self, db_session, sample_slot):
        """Test eliminación de franja"""
        slot_id = sample_slot.id
        delete_slot(db_session, sample_slot)
        
        assert get_slot(db_session, slot_id) is None

