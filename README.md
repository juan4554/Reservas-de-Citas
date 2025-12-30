# Reserva Sport

Sistema de reservas para instalaciones deportivas. Basicamente, los usuarios pueden ver que instalaciones hay disponibles, consultar horarios y hacer reservas.

Es un proyecto que hice para mi TFG, asi que puede tener algunos detalles por pulir, pero funciona bien.

## Cómo empezar

### Opción fácil: Docker

Si tienes Docker instalado, esto es lo más rápido:

1. Primero asegurate de que Docker Desktop este corriendo. En Windows, buscalo en el menu de inicio y abrelo. Deberias ver el icono de la ballena en la bandeja del sistema.

2. Clona el repo:
   ```bash
   git clone <url-del-repositorio>
   cd Reservas-de-Citas
   ```

3. Levanta todo:
   ```bash
   docker-compose up -d
   ```

4. Espera unos segundos (la primera vez tarda un poco) y abre:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Docs de la API: http://localhost:8000/docs (solo si esta en modo desarrollo)

Para ver si todo esta bien:
```bash
docker-compose ps
docker-compose logs -f
```

## Requisitos

- Docker Desktop (si vas a usar Docker)
- Python 3.11 o superior (para desarrollo local del backend)
- Node.js 20 o superior (para el frontend)

## Desarrollo local (sin Docker)

Si prefieres no usar Docker, puedes correrlo localmente (aunque Docker es mas facil):

### Backend

```bash
#crear el entorno virtual
python -m venv venv

#activarlo
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

#instalar dependencias
pip install -r requirements.txt

#aplicar migraciones
alembic upgrade head

#arrancar el servidor
uvicorn app.main:app --reload
```

El backend corre en http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend corre en http://localhost:5173 (Vite usa este puerto por defecto, aunque puedes cambiarlo)

## Configuración

### Variables de entorno (o environment variables)

Crea un archivo `.env` en la raiz. Si hay un `.env.example`, puedes copiarlo:

```env
DATABASE_URL=sqlite:///./reserva.db
JWT_SECRET=pon-aqui-algo-seguro
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Base de datos

Por defecto usa SQLite, que esta bien para desarrollo. Si quieres usar PostgreSQL en produccion:

1. Descomenta la parte del servicio `db` en `docker-compose.yml`
2. Cambia el `DATABASE_URL` en el `.env` a algo como:
   ```
   DATABASE_URL=postgresql://reservas:reservas123@db:5432/reservas
   ```

## Scripts que pueden ser útiles

### Generar slots semanales (horarios)

Para crear los horarios disponibles de la semana (los slots):

```bash
#genera slots para 7 dias (una semana)
python scripts/generate_weekly_slots.py

#para 14 dias
python scripts/generate_weekly_slots.py --days 14

#desde una fecha especifica
python scripts/generate_weekly_slots.py --start-date 2025-01-01

#solo para una instalacion
python scripts/generate_weekly_slots.py --facility-id 1
```

Hay otro script mas avanzado si necesitas configurar horarios diferentes por instalacion:

```bash
python scripts/generate_weekly_slots_config.py --config scripts/slots_config.example.json
```

### Resetear password de admin (si se te olvida)

Si te olvidaste la contrasena del admin:

```bash
python reset_admin.py
```

## Tests

```bash
#todos los tests
pytest

#con cobertura (genera un reporte HTML)
pytest --cov=app --cov-report=html

#un archivo especifico
pytest tests/test_models.py
```

## Migraciones de base de datos (database migrations)

```bash
#crear una nueva migracion
alembic revision --autogenerate -m "descripcion de lo que cambias"

#aplicar todas las migraciones pendientes
alembic upgrade head

#revertir la ultima migracion (por si acaso)
alembic downgrade -1
```

## Comandos Docker que uso mucho (los mas utiles)

```bash
#construir las imagenes
docker-compose build

#levantar todo
docker-compose up -d

#ver logs (util para debug)
docker-compose logs -f backend
docker-compose logs -f frontend

#parar todo
docker-compose down

#reiniciar solo el backend
docker-compose restart backend

#ejecutar algo dentro del contenedor
docker-compose exec backend alembic upgrade head
```

## Problemas comunes (troubleshooting)

### Docker no arranca

- Mira si el icono de Docker esta en la bandeja del sistema
- En Windows, verifica que tengas WSL 2: `wsl --list --verbose`
- A veces reiniciar Docker Desktop ayuda

### Puerto ocupado

Si el 8000 o 3000 ya estan en uso, cambia los puertos en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  #backend ahora en 8001
  - "3001:80"    #frontend en 3001
```

### Error "database is locked"

SQLite no se lleva bien con multiples procesos escribiendo a la vez. 
Soluciones:
- Asegurate de que solo un proceso este accediendo a la BD
- Para produccion, mejor usa PostgreSQL (descomenta el servicio `db`)

### No encuentra módulos

A veces Docker se queda con cache viejo. Prueba:

```bash
#reconstruir sin cache
docker-compose build --no-cache backend
```

## Estructura del proyecto (como esta organizado)

```
Reservas-de-Citas/
├── app/                    #backend con FastAPI
│   ├── api/               #los endpoints
│   ├── core/              #config y seguridad
│   ├── models/            #modelos de BD
│   ├── schemas/           #schemas de Pydantic
│   └── utils/             #funciones auxiliares
├── frontend/              #React + TypeScript
│   ├── src/
│   │   ├── components/   #componentes
│   │   ├── pages/        #paginas
│   │   └── lib/          #API client y utilidades
│   └── public/
├── scripts/               #scripts utiles
├── tests/                 #tests
├── alembic/              #migraciones
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Credenciales por defecto (default credentials)

**Admin:**
- Email: `admin@test.local.es`
- Password: `admin123`

**OJO:** Cambia esto en produccion, obviamente.

## Desplegar en produccion

1. Configura el `.env`:
   ```env
   ENVIRONMENT=production
   DEBUG=False
   JWT_SECRET=<genera-algo-seguro>
   DATABASE_URL=postgresql://user:pass@db:5432/reservas
   CORS_ORIGINS=https://tudominio.com
   ```

2. Descomenta PostgreSQL en `docker-compose.yml`

3. Build y up:
   ```bash
   #construir
   docker-compose build
   #levantar
   docker-compose up -d
   ```

4. Migraciones:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## Stack tecnologico

**Backend:**
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT para auth

**Frontend:**
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router

**DevOps:**
- Docker
- Docker Compose

## Licencia (no tiene)

Es un proyecto de TFG, asi que no hay licencia especifica. Sientete libre de hacer fork y usarlo como quieras.

## Contribuciones (si quieres ayudar)

Es un proyecto academico, pero si quieres mejorarlo o usarlo como base, adelante. Si encuentras bugs o tienes sugerencias, puedes abrir un issue.

## Si algo no funciona (help)

1. Revisa la seccion de problemas comunes arriba
2. Mira los logs: `docker-compose logs -f`
3. Verifica que Docker Desktop este corriendo
4. Si nada funciona, puede que sea un problema de configuracion o de version de algo
