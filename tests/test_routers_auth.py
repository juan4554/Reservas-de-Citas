"""
Tests unitarios para endpoints de autenticación
"""
import pytest
from app.models.user import UserRole


class TestAuthRouter:
    """Tests para el router de autenticación"""
    
    def test_register_user(self, client):
        """Test registro de nuevo usuario"""
        response = client.post(
            "/auth/register",
            json={
                "nombre": "Nuevo Usuario",
                "email": "nuevo@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "nuevo@example.com"
        assert data["nombre"] == "Nuevo Usuario"
        assert data["rol"] == "cliente"
        assert "id" in data
        assert "hashed_password" not in data
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test que no se puede registrar email duplicado"""
        response = client.post(
            "/auth/register",
            json={
                "nombre": "Otro Usuario",
                "email": sample_user.email,
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "ya registrado" in response.json()["detail"].lower()
    
    def test_register_invalid_data(self, client):
        """Test registro con datos inválidos"""
        response = client.post(
            "/auth/register",
            json={
                "nombre": "A",  # Muy corto
                "email": "invalid-email",
                "password": "123"  # Muy corto
            }
        )
        
        assert response.status_code == 422
    
    def test_login_success(self, client, sample_user):
        """Test login exitoso"""
        response = client.post(
            "/auth/login",
            data={
                "username": sample_user.email,
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_wrong_password(self, client, sample_user):
        """Test login con contraseña incorrecta"""
        response = client.post(
            "/auth/login",
            data={
                "username": sample_user.email,
                "password": "wrong_password"
            }
        )
        
        assert response.status_code == 401
        assert "inválidas" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login con usuario inexistente"""
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
    
    def test_me_endpoint(self, client, auth_headers):
        """Test endpoint /me para obtener usuario actual"""
        response = client.get("/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "nombre" in data
        assert "rol" in data
    
    def test_me_endpoint_unauthorized(self, client):
        """Test endpoint /me sin autenticación"""
        response = client.get("/auth/me")
        
        assert response.status_code == 403

