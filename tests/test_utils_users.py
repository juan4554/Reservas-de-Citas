"""
Tests unitarios para utilidades de usuarios
"""
import pytest
from app.utils.users import get_user_by_email, create_user
from app.models.user import User, UserRole
from app.core.security import verify_password


class TestUserUtils:
    """Tests para funciones de utilidad de usuarios"""
    
    def test_get_user_by_email_exists(self, db_session, sample_user):
        """Test obtener usuario por email existente"""
        user = get_user_by_email(db_session, sample_user.email)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email
    
    def test_get_user_by_email_not_exists(self, db_session):
        """Test obtener usuario por email inexistente"""
        user = get_user_by_email(db_session, "nonexistent@example.com")
        
        assert user is None
    
    def test_create_user(self, db_session):
        """Test creación de usuario"""
        user = create_user(
            db_session,
            nombre="Nuevo Usuario",
            email="nuevo@example.com",
            password="password123"
        )
        
        assert user.id is not None
        assert user.nombre == "Nuevo Usuario"
        assert user.email == "nuevo@example.com"
        assert user.rol == UserRole.cliente
        assert verify_password("password123", user.hashed_password)
    
    def test_create_user_with_role(self, db_session):
        """Test creación de usuario con rol específico"""
        user = create_user(
            db_session,
            nombre="Admin User",
            email="admin@example.com",
            password="admin123",
            rol=UserRole.admin
        )
        
        assert user.rol == UserRole.admin
    
    def test_create_user_duplicate_email(self, db_session, sample_user):
        """Test que no se puede crear usuario con email duplicado"""
        with pytest.raises(Exception):  # Puede ser IntegrityError o similar
            create_user(
                db_session,
                nombre="Otro Usuario",
                email=sample_user.email,
                password="password123"
            )

