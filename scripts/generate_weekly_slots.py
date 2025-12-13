"""
Script para generar slots semanales para todas las instalaciones
Uso: python scripts/generate_weekly_slots.py [--days N] [--start-date YYYY-MM-DD]
"""
import sys
import os
import argparse
from datetime import date, time, timedelta
from typing import List, Tuple

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Horarios típicos de clases (puedes modificar estos)
DEFAULT_TIME_SLOTS = [
    (time(9, 0), time(10, 0)),
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(17, 0), time(18, 0)),
    (time(18, 0), time(19, 0)),
    (time(19, 0), time(20, 0)),
    (time(20, 0), time(21, 0)),
]

# Capacidad por defecto
DEFAULT_CAPACITY = 20


def login(email: str, password: str) -> str:
    """Iniciar sesión y obtener token"""
    response = requests.post(
        f"{API_URL}/auth/login",
        data={
            "username": email,
            "password": password,
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Error al iniciar sesión: {response.text}")
    
    return response.json()["access_token"]


def get_facilities(token: str) -> List[dict]:
    """Obtener todas las instalaciones"""
    response = requests.get(
        f"{API_URL}/facilities",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Error al obtener instalaciones: {response.text}")
    
    return response.json()


def create_slot(
    token: str,
    instalacion_id: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    capacidad: int = DEFAULT_CAPACITY
) -> dict | None:
    """Crear un slot"""
    response = requests.post(
        f"{API_URL}/slots",
        json={
            "instalacion_id": instalacion_id,
            "fecha": fecha.isoformat(),
            "hora_inicio": hora_inicio.strftime("%H:%M:%S"),
            "hora_fin": hora_fin.strftime("%H:%M:%S"),
            "capacidad": capacidad,
            "plazas_disponibles": capacidad
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 409:
        # Slot ya existe, no es error
        return None
    else:
        print(f"  [WARN] Error al crear slot {hora_inicio}-{hora_fin}: {response.text}")
        return None


def generate_weekly_slots(
    token: str,
    facility_id: int,
    facility_name: str,
    start_date: date,
    days: int,
    time_slots: List[Tuple[time, time]],
    capacity: int = DEFAULT_CAPACITY
) -> Tuple[int, int]:
    """Generar slots para una instalación durante N días"""
    created = 0
    skipped = 0
    
    print(f"\n[INFO] Generando slots para: {facility_name} (ID: {facility_id})")
    print(f"   Periodo: {start_date} a {start_date + timedelta(days=days-1)}")
    print(f"   Horarios: {len(time_slots)} por dia")
    
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        
        for hora_inicio, hora_fin in time_slots:
            result = create_slot(
                token,
                facility_id,
                current_date,
                hora_inicio,
                hora_fin,
                capacity
            )
            
            if result:
                created += 1
            else:
                skipped += 1
    
    print(f"   [OK] Creados: {created}, [SKIP] Omitidos (ya existian): {skipped}")
    return created, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Generar slots semanales para todas las instalaciones"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Número de días a generar (default: 7)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Fecha de inicio (YYYY-MM-DD). Por defecto: hoy"
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=DEFAULT_CAPACITY,
        help=f"Capacidad por slot (default: {DEFAULT_CAPACITY})"
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
        help="Contraseña del administrador"
    )
    parser.add_argument(
        "--facility-id",
        type=int,
        default=None,
        help="ID de instalación específica (opcional, si no se especifica genera para todas)"
    )
    
    args = parser.parse_args()
    
    # Determinar fecha de inicio
    if args.start_date:
        start_date = date.fromisoformat(args.start_date)
    else:
        start_date = date.today()
    
    print("Generador de Slots Semanales")
    print("=" * 50)
    print(f"Fecha inicio: {start_date}")
    print(f"Dias a generar: {args.days}")
    print(f"Capacidad por slot: {args.capacity}")
    print(f"Horarios por dia: {len(DEFAULT_TIME_SLOTS)}")
    print("=" * 50)
    
    # Iniciar sesión
    print("\n[INFO] Iniciando sesion...")
    try:
        token = login(args.email, args.password)
        print("[OK] Sesion iniciada correctamente")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    
    # Obtener instalaciones
    print("\n[INFO] Obteniendo instalaciones...")
    try:
        facilities = get_facilities(token)
        print(f"[OK] Encontradas {len(facilities)} instalaciones")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    
    # Filtrar por facility_id si se especifica
    if args.facility_id:
        facilities = [f for f in facilities if f["id"] == args.facility_id]
        if not facilities:
            print(f"[ERROR] No se encontro la instalacion con ID {args.facility_id}")
            sys.exit(1)
    
    # Generar slots para cada instalación
    total_created = 0
    total_skipped = 0
    
    for facility in facilities:
        created, skipped = generate_weekly_slots(
            token,
            facility["id"],
            facility["nombre"],
            start_date,
            args.days,
            DEFAULT_TIME_SLOTS,
            args.capacity
        )
        total_created += created
        total_skipped += skipped
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    print(f"[OK] Slots creados: {total_created}")
    print(f"[SKIP] Slots omitidos (ya existian): {total_skipped}")
    print(f"[TOTAL] Total procesado: {total_created + total_skipped}")
    print("=" * 50)
    print("\n[OK] Proceso completado!")


if __name__ == "__main__":
    main()

