@echo off
REM Script batch para Windows - Generar slots semanales (config avanzado)
REM Uso: generate_weekly_slots_config.bat [dias] [fecha_inicio]

setlocal

set DAYS=%1
if "%DAYS%"=="" set DAYS=7

set START_DATE=%2

REM Intentar activar entorno virtual si existe
if exist "..\.venv\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call ..\.venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo [WARN] No se encontro entorno virtual. Usando Python del sistema.
    echo [INFO] Asegurate de tener instaladas las dependencias: requests y python-dotenv
)

REM Verificar si las dependencias estan instaladas
python -c "import requests" 2>nul
if errorlevel 1 (
    echo [ERROR] El modulo 'requests' no esta instalado.
    echo [INFO] Instalando dependencias...
    pip install requests python-dotenv
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias.
        echo [INFO] Ejecuta manualmente: pip install requests python-dotenv
        pause
        exit /b 1
    )
)

REM Ejecutar el script
echo [INFO] Ejecutando script de generacion de slots...
if "%START_DATE%"=="" (
    python scripts\generate_weekly_slots_config.py --days %DAYS%
) else (
    python scripts\generate_weekly_slots_config.py --days %DAYS% --start-date %START_DATE%
)

if errorlevel 1 (
    echo.
    echo [ERROR] El script fallo. Verifica:
    echo   1. Que el backend este corriendo en http://localhost:8000
    echo   2. Que tengas las credenciales correctas (admin@test.local.es / admin123)
    echo   3. Que tengas las dependencias instaladas: pip install requests python-dotenv
    pause
    exit /b 1
)

echo.
echo [OK] Script completado exitosamente!
pause

