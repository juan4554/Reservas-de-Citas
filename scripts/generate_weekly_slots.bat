@echo off
REM Script batch para Windows - Generar slots semanales
REM Uso: generate_weekly_slots.bat [dias] [fecha_inicio]

set DAYS=%1
if "%DAYS%"=="" set DAYS=7

set START_DATE=%2
if "%START_DATE%"=="" (
    python scripts\generate_weekly_slots.py --days %DAYS%
) else (
    python scripts\generate_weekly_slots.py --days %DAYS% --start-date %START_DATE%
)

pause

