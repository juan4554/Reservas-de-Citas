@echo off
REM Script de inicio rápido para Windows

echo Iniciando Reservas de Citas...

REM Verificar si existe .env
if not exist .env (
    echo Creando archivo .env...
    if exist .env.example (
        copy .env.example .env
        echo Archivo .env creado. Por favor, editalo con tus configuraciones.
    ) else (
        echo Creando .env basico...
        (
            echo DATABASE_URL=sqlite:///./reserva.db
            echo JWT_SECRET=change-this-secret-key-in-production
            echo ACCESS_TOKEN_EXPIRE_MINUTES=60
            echo ENVIRONMENT=development
            echo DEBUG=True
            echo CORS_ORIGINS=http://localhost:3000,http://localhost:5173
            echo LOG_LEVEL=INFO
        ) > .env
    )
)

REM Verificar si existe venv
if not exist venv (
    if not exist .venv (
        echo Creando entorno virtual...
        python -m venv venv
    )
)

REM Activar venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -q -r requirements.txt

REM Verificar base de datos
if not exist reserva.db (
    echo Base de datos no encontrada. Ejecutando migraciones...
    alembic upgrade head
)

echo.
echo Todo listo!
echo.
echo Para iniciar el servidor:
echo   uvicorn app.main:app --reload
echo.
echo Para ejecutar tests:
echo   pytest
echo.
echo Para usar Docker:
echo   docker-compose up -d
echo.

pause

