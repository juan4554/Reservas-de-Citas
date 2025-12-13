#!/bin/bash
# Script bash para Linux/Mac - Generar slots semanales
# Uso: ./generate_weekly_slots.sh [dias] [fecha_inicio]

DAYS=${1:-7}
START_DATE=${2:-}

if [ -z "$START_DATE" ]; then
    python scripts/generate_weekly_slots.py --days "$DAYS"
else
    python scripts/generate_weekly_slots.py --days "$DAYS" --start-date "$START_DATE"
fi

