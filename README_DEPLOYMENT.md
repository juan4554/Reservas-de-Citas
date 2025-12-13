# Guía de Deployment

## Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.11+ (para desarrollo local)
- Node.js 20+ (para desarrollo frontend)

## Deployment con Docker

### 1. Configurar Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
DATABASE_URL=sqlite:///./reserva.db
JWT_SECRET=tu-secreto-super-seguro-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=http://localhost:3000,https://tudominio.com
```

### 2. Construir y Levantar Contenedores

```bash
# Construir imágenes
docker-compose build

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3. Verificar Deployment

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs (solo en modo debug)
- Health Check: http://localhost:8000/health

### 4. Ejecutar Migraciones

```bash
# Dentro del contenedor
docker-compose exec backend alembic upgrade head

# O desde fuera
docker-compose exec backend alembic upgrade head
```

## Desarrollo Local

### Backend

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload

# Ejecutar tests
pytest
pytest --cov=app
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_models.py
```

## Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## Producción con PostgreSQL

1. Descomenta el servicio `db` en `docker-compose.yml`
2. Actualiza `DATABASE_URL` en `.env`:
   ```
   DATABASE_URL=postgresql://reservas:reservas123@db:5432/reservas
   ```
3. Reinicia los contenedores:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Troubleshooting

### Error: Puerto ya en uso
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

### Error: Base de datos bloqueada (SQLite)
- Asegúrate de que solo un proceso accede a la BD
- En producción, usa PostgreSQL

### Error: Permisos Docker
```bash
# Linux: añadir usuario al grupo docker
sudo usermod -aG docker $USER
```

## Comandos Útiles

```bash
# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar servicio
docker-compose restart backend

# Ejecutar comando en contenedor
docker-compose exec backend python -c "from app.core.config import settings; print(settings.database_url)"

# Limpiar todo
docker-compose down -v
docker system prune -a
```

