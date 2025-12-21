# Scripts de Utilidad

## generate_weekly_slots.py

Script para generar slots semanales para todas las instalaciones a través de la API.

### Uso Básico

```bash
# Generar slots para la próxima semana (7 días desde hoy)
python scripts/generate_weekly_slots.py

# Generar slots para 14 días
python scripts/generate_weekly_slots.py --days 14

# Generar slots desde una fecha específica
python scripts/generate_weekly_slots.py --start-date 2024-12-20

# Generar slots para una instalación específica
python scripts/generate_weekly_slots.py --facility-id 1

# Cambiar capacidad por defecto
python scripts/generate_weekly_slots.py --capacity 30

# Usar credenciales diferentes
python scripts/generate_weekly_slots.py --email admin@example.com --password mi_password
```

### Opciones

- `--days N`: Número de días a generar (default: 7)
- `--start-date YYYY-MM-DD`: Fecha de inicio (default: hoy)
- `--capacity N`: Capacidad por slot (default: 20)
- `--email EMAIL`: Email del admin (default: admin@test.local.es)
- `--password PASSWORD`: Contraseña del admin (default: admin123)
- `--facility-id ID`: ID de instalación específica (opcional)

### Horarios por Defecto

El script genera slots con estos horarios:
- 09:00 - 10:00
- 10:00 - 11:00
- 11:00 - 12:00
- 17:00 - 18:00
- 18:00 - 19:00
- 19:00 - 20:00
- 20:00 - 21:00

### Ejemplos

```bash
# Generar slots para las próximas 2 semanas
python scripts/generate_weekly_slots.py --days 14

# Generar slots solo para la instalación ID 1
python scripts/generate_weekly_slots.py --facility-id 1

# Generar slots desde el 1 de enero con capacidad de 25
python scripts/generate_weekly_slots.py --start-date 2025-01-01 --capacity 25
```

### Scripts de Acceso Rápido

**Windows:**
```batch
scripts\generate_weekly_slots.bat 7
scripts\generate_weekly_slots.bat 14 2025-01-01
```

**Linux/Mac:**
```bash
chmod +x scripts/generate_weekly_slots.sh
./scripts/generate_weekly_slots.sh 7
./scripts/generate_weekly_slots.sh 14 2025-01-01
```

## generate_weekly_slots_config.py

Script avanzado con configuración personalizable mediante archivo JSON.

### Uso Básico

```bash
# Generar slots para la próxima semana (7 días desde hoy)
python scripts/generate_weekly_slots_config.py

# Generar slots para 14 días
python scripts/generate_weekly_slots_config.py --days 14

# Generar slots desde una fecha específica
python scripts/generate_weekly_slots_config.py --start-date 2024-12-20

# Generar slots para una instalación específica
python scripts/generate_weekly_slots_config.py --facility-id 1

# Usar credenciales diferentes
python scripts/generate_weekly_slots_config.py --email admin@example.com --password mi_password

# Usar archivo de configuración personalizado
python scripts/generate_weekly_slots_config.py --config slots_config.example.json
```

### Scripts de Acceso Rápido (Windows)

**Desde el directorio raíz del proyecto:**
```batch
scripts\generate_weekly_slots_config.bat
scripts\generate_weekly_slots_config.bat 14
scripts\generate_weekly_slots_config.bat 7 2025-01-01
```

### Solución de Problemas

**Error: "No module named 'requests'"**
```bash
pip install requests python-dotenv
```

**Error: "Connection refused" o "Failed to connect"**
- Verifica que el backend esté corriendo: `docker-compose up -d backend`
- Verifica que la API esté accesible: `curl http://localhost:8000/health`

**Error: "401 Unauthorized"**
- Verifica las credenciales del admin (por defecto: `admin@test.local.es` / `admin123`)
- Puedes cambiar las credenciales con `--email` y `--password`

### Uso con Configuración

```bash
# Usar archivo de configuración
python scripts/generate_weekly_slots_config.py --config scripts/slots_config.example.json

# Generar con configuración personalizada
python scripts/generate_weekly_slots_config.py --config mi_config.json --days 14
```

### Formato del Archivo de Configuración

Ver `scripts/slots_config.example.json` para un ejemplo completo.

**Características:**
- Horarios personalizados por instalación
- Capacidad diferente por instalación
- Excluir días de la semana (ej: domingos)
- Configuración centralizada

### Ejemplo de Configuración

```json
{
  "time_slots": [
    {"start": "09:00", "end": "10:00"},
    {"start": "18:00", "end": "19:00"}
  ],
  "capacity": 20,
  "exclude_days": [6],
  "facility_overrides": {
    "1": {
      "capacity": 30,
      "time_slots": [
        {"start": "08:00", "end": "09:00"},
        {"start": "09:00", "end": "10:00"}
      ]
    }
  }
}
```

### Notas

- El script omite slots que ya existen (no genera duplicados)
- Requiere que el backend esté corriendo
- Necesita credenciales de administrador
- Los slots se crean con `plazas_disponibles` igual a `capacidad`
- Puedes ejecutar el script periódicamente (ej: cada lunes) para generar la semana siguiente

