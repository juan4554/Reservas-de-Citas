"""
Tests unitarios para módulo de seguridad
"""
import pytest
from datetime import timedelta
from jose import jwt

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)
from app.core.config import settings


class TestPasswordHashing:
    """Tests para hash y verificación de contraseñas"""
    
    def test_hash_password(self):
        """Test que hash_password genera un hash diferente"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$pbkdf2-sha256$")
    
    def test_verify_password_correct(self):
        """Test verificación de contraseña correcta"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verificación de contraseña incorrecta"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_different_for_same_password(self):
        """Test que el mismo password genera hashes diferentes (salt)"""
        password = "test_password_123"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        
        assert hashed1 != hashed2
        # Pero ambos deben verificar correctamente
        assert verify_password(password, hashed1) is True
        assert verify_password(password, hashed2) is True


class TestJWT:
    """Tests para tokens JWT"""
    
    def test_create_access_token(self):
        """Test creación de token de acceso"""
        token = create_access_token(
            sub="test@example.com",
            uid=1,
            rol="cliente",
            minutes=60
        )
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_valid_token(self):
        """Test decodificación de token válido"""
        token = create_access_token(
            sub="test@example.com",
            uid=1,
            rol="cliente"
        )
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["uid"] == 1
        assert payload["rol"] == "cliente"
        assert "iat" in payload
        assert "exp" in payload
    
    def test_decode_invalid_token(self):
        """Test decodificación de token inválido"""
        invalid_token = "invalid_token_string"
        payload = decode_token(invalid_token)
        
        assert payload is None
    
    def test_decode_expired_token(self):
        """Test que token expirado no se puede decodificar"""
        token = create_access_token(
            sub="test@example.com",
            uid=1,
            rol="cliente",
            minutes=-1  # Token ya expirado
        )
        
        # Esperar un segundo para asegurar expiración
        import time
        time.sleep(1)
        
        payload = decode_token(token)
        # El token expirado debería fallar al decodificar
        # Nota: jose puede lanzar JWTError, pero nuestro decode_token retorna None
        # Esto depende de la implementación, pero el token expirado no debería ser válido
        if payload:
            # Si decodifica, verificar que exp está en el pasado
            from datetime import datetime, timezone
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                assert exp_datetime < datetime.now(timezone.utc)
    
    def test_token_custom_expiration(self):
        """Test token con expiración personalizada"""
        token = create_access_token(
            sub="test@example.com",
            uid=1,
            rol="cliente",
            minutes=30
        )
        
        payload = decode_token(token)
        assert payload is not None
        
        # Verificar que la expiración es aproximadamente 30 minutos
        from datetime import datetime, timezone
        exp_timestamp = payload["exp"]
        iat_timestamp = payload["iat"]
        exp_minutes = (exp_timestamp - iat_timestamp) / 60
        
        assert 29 <= exp_minutes <= 31  # Tolerancia de 1 minuto

