"""
Script para programar la generación automática de slots semanales
Puede ejecutarse como tarea programada (cron en Linux, Task Scheduler en Windows)
"""
import sys
import os
from datetime import date, timedelta

# Importar el script principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_weekly_slots import main as generate_main
import argparse


def main():
    """
    Genera slots para la próxima semana automáticamente.
    Ideal para ejecutar cada lunes o domingo.
    """
    parser = argparse.ArgumentParser(
        description="Generar slots para la proxima semana automaticamente"
    )
    parser.add_argument(
        "--weeks-ahead",
        type=int,
        default=1,
        help="Semanas adelante a generar (default: 1)"
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=20,
        help="Capacidad por slot"
    )
    parser.add_argument(
        "--email",
        type=str,
        default="admin@test.local.es",
        help="Email del administrador"
    )
    parser.add_argument(
        "--password",
        type=str,
        default="admin123",
        help="Contrasena del administrador"
    )
    
    args = parser.parse_args()
    
    # Calcular fecha de inicio (próximo lunes o hoy si es lunes)
    today = date.today()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # Si es lunes, generar para el próximo lunes
    
    start_date = today + timedelta(days=days_until_monday)
    days_to_generate = args.weeks_ahead * 7
    
    print(f"[INFO] Generando slots para {args.weeks_ahead} semana(s) a partir del {start_date}")
    
    # Simular argumentos para el script principal
    sys.argv = [
        "generate_weekly_slots.py",
        "--days", str(days_to_generate),
        "--start-date", start_date.isoformat(),
        "--capacity", str(args.capacity),
        "--email", args.email,
        "--password", args.password
    ]
    
    generate_main()


if __name__ == "__main__":
    main()

