# Programación Automática de Slots

## Windows Task Scheduler

Para ejecutar automáticamente cada lunes:

1. Abre "Programador de tareas" (Task Scheduler)
2. Crea una tarea básica
3. Configura:
   - **Nombre**: Generar Slots Semanales
   - **Desencadenador**: Semanal, Lunes, 8:00 AM
   - **Acción**: Iniciar programa
   - **Programa**: `python`
   - **Argumentos**: `C:\ruta\al\proyecto\scripts\schedule_weekly_slots.py`
   - **Iniciar en**: `C:\ruta\al\proyecto`

## Linux Cron

Añade a tu crontab (`crontab -e`):

```bash
# Generar slots cada lunes a las 8:00 AM
0 8 * * 1 cd /ruta/al/proyecto && python scripts/schedule_weekly_slots.py
```

## Docker Container

Si quieres ejecutarlo dentro del contenedor:

```bash
# Ejecutar manualmente
docker-compose exec backend python scripts/schedule_weekly_slots.py

# O crear un servicio separado en docker-compose.yml
```

## Ejecución Manual

```bash
# Generar para la próxima semana
python scripts/schedule_weekly_slots.py

# Generar para las próximas 2 semanas
python scripts/schedule_weekly_slots.py --weeks-ahead 2
```

