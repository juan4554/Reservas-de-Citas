"""
Script avanzado para generar slots con configuración personalizada
Permite definir horarios diferentes por instalación o día de la semana
"""
import sys
import os
import json
import argparse
from datetime import date, time, timedelta
from typing import List, Tuple, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configuración por defecto
DEFAULT_CONFIG = {
    "time_slots": [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:00", "end": "11:00"},
        {"start": "11:00", "end": "12:00"},
        {"start": "17:00", "end": "18:00"},
        {"start": "18:00", "end": "19:00"},
        {"start": "19:00", "end": "20:00"},
        {"start": "20:00", "end": "21:00"},
    ],
    "capacity": 20,
    "exclude_days": [],  # Días de la semana a excluir (0=Lunes, 6=Domingo)
    "facility_overrides": {}  # {facility_id: {"capacity": 30, "time_slots": [...]}}
}


def parse_time(time_str: str) -> time:
    """Parse time string HH:MM to time object"""
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))


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
        raise Exception(f"Error al iniciar sesion: {response.text}")
    
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
    capacidad: int
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
        return None  # Ya existe
    else:
        return None


def get_time_slots_for_facility(
    facility_id: int,
    config: dict,
    default_slots: List[Dict[str, str]]
) -> List[Tuple[time, time]]:
    """Obtener horarios para una instalación específica"""
    override = config.get("facility_overrides", {}).get(facility_id, {})
    
    if "time_slots" in override:
        slots = override["time_slots"]
    else:
        slots = config.get("time_slots", default_slots)
    
    return [
        (parse_time(s["start"]), parse_time(s["end"]))
        for s in slots
    ]


def should_skip_day(date_obj: date, config: dict) -> bool:
    """Verificar si se debe saltar un día (ej: domingos)"""
    weekday = date_obj.weekday()  # 0=Lunes, 6=Domingo
    exclude_days = config.get("exclude_days", [])
    return weekday in exclude_days


def generate_slots(
    token: str,
    facility_id: int,
    facility_name: str,
    start_date: date,
    days: int,
    config: dict
) -> Tuple[int, int]:
    """Generar slots para una instalación"""
    created = 0
    skipped = 0
    
    capacity = config.get("facility_overrides", {}).get(facility_id, {}).get("capacity") or config.get("capacity", 20)
    time_slots = get_time_slots_for_facility(facility_id, config, DEFAULT_CONFIG["time_slots"])
    
    print(f"\n[INFO] {facility_name} (ID: {facility_id})")
    print(f"   Periodo: {start_date} a {start_date + timedelta(days=days-1)}")
    print(f"   Capacidad: {capacity}")
    print(f"   Horarios: {len(time_slots)} por dia")
    
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        
        # Saltar días excluidos
        if should_skip_day(current_date, config):
            continue
        
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
    
    print(f"   [OK] Creados: {created}, [SKIP] Omitidos: {skipped}")
    return created, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Generar slots semanales con configuracion personalizada"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Archivo JSON con configuracion (opcional)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Numero de dias a generar (default: 7)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Fecha de inicio (YYYY-MM-DD). Por defecto: hoy"
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
    parser.add_argument(
        "--facility-id",
        type=int,
        default=None,
        help="ID de instalacion especifica (opcional)"
    )
    
    args = parser.parse_args()
    
    # Cargar configuración
    config = DEFAULT_CONFIG.copy()
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            config.update(user_config)
    
    # Determinar fecha de inicio
    if args.start_date:
        start_date = date.fromisoformat(args.start_date)
    else:
        start_date = date.today()
    
    print("Generador de Slots Semanales (Avanzado)")
    print("=" * 60)
    print(f"Fecha inicio: {start_date}")
    print(f"Dias a generar: {args.days}")
    print(f"Capacidad por defecto: {config.get('capacity', 20)}")
    print(f"Horarios por defecto: {len(config.get('time_slots', []))}")
    if config.get("exclude_days"):
        print(f"Dias excluidos: {config['exclude_days']}")
    print("=" * 60)
    
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
    
    # Generar slots
    total_created = 0
    total_skipped = 0
    
    for facility in facilities:
        created, skipped = generate_slots(
            token,
            facility["id"],
            facility["nombre"],
            start_date,
            args.days,
            config
        )
        total_created += created
        total_skipped += skipped
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"[OK] Slots creados: {total_created}")
    print(f"[SKIP] Slots omitidos: {total_skipped}")
    print(f"[TOTAL] Total procesado: {total_created + total_skipped}")
    print("=" * 60)
    print("\n[OK] Proceso completado!")


if __name__ == "__main__":
    main()

