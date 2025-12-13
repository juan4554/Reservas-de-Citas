# Guía de Troubleshooting

## Problemas Comunes con Docker

### Error: "unable to get image" o "cannot connect to Docker daemon"

**Síntoma:**
```
unable to get image 'reservas-de-citas-backend': error during connect: 
Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.48/images/...": 
open //./pipe/dockerDesktopLinuxEngine: El sistema no puede encontrar el archivo especificado.
```

**Causa:** Docker Desktop no está corriendo o no está instalado correctamente.

**Solución:**

1. **Verificar que Docker Desktop esté instalado:**
   - Abre Docker Desktop desde el menú de inicio
   - Espera a que aparezca el ícono de Docker en la bandeja del sistema (systray)
   - Debe mostrar "Docker Desktop is running"

2. **Verificar que Docker esté corriendo:**
   ```powershell
   docker ps
   ```
   Si funciona, verás una lista (puede estar vacía). Si da error, Docker no está corriendo.

3. **Reiniciar Docker Desktop:**
   - Cierra Docker Desktop completamente
   - Vuelve a abrirlo
   - Espera a que termine de iniciar

4. **Verificar la instalación:**
   ```powershell
   docker --version
   docker-compose --version
   ```

### Error: "Port already in use"

**Síntoma:**
```
Error: bind: address already in use
```

**Solución:**

1. **Verificar qué está usando el puerto:**
   ```powershell
   # Windows PowerShell
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   ```

2. **Cambiar los puertos en docker-compose.yml:**
   ```yaml
   ports:
     - "8001:8000"  # Backend en puerto 8001
     - "3001:80"     # Frontend en puerto 3001
   ```

3. **O detener el proceso que usa el puerto:**
   ```powershell
   # Encontrar el PID del proceso
   netstat -ano | findstr :8000
   # Matar el proceso (reemplaza PID con el número)
   taskkill /PID <PID> /F
   ```

### Error: "Build failed" o problemas al construir imágenes

**Síntoma:**
```
ERROR: failed to solve: process "/bin/sh -c pip install..." did not complete successfully
```

**Soluciones:**

1. **Limpiar caché de Docker:**
   ```powershell
   docker system prune -a
   ```

2. **Reconstruir sin caché:**
   ```powershell
   docker-compose build --no-cache
   ```

3. **Verificar que requirements.txt esté correcto:**
   ```powershell
   # Probar instalación local
   pip install -r requirements.txt
   ```

### Error: "Database is locked" (SQLite)

**Síntoma:**
```
sqlite3.OperationalError: database is locked
```

**Causa:** SQLite no maneja bien múltiples escritores concurrentes.

**Soluciones:**

1. **Usar PostgreSQL en producción** (recomendado):
   - Descomenta el servicio `db` en `docker-compose.yml`
   - Actualiza `DATABASE_URL` en `.env`

2. **Para desarrollo, asegúrate de que solo un proceso accede a la BD:**
   - No corras el servidor localmente mientras Docker está corriendo
   - O usa volúmenes separados

### Error: "Module not found" en el contenedor

**Síntoma:**
```
ModuleNotFoundError: No module named 'app'
```

**Solución:**

1. **Verificar que el Dockerfile copie todo correctamente:**
   ```dockerfile
   COPY . .
   ```

2. **Reconstruir la imagen:**
   ```powershell
   docker-compose build --no-cache backend
   ```

### Error: "Permission denied" en Linux/Mac

**Síntoma:**
```
permission denied while trying to connect to the Docker daemon socket
```

**Solución (Linux):**
```bash
# Añadir usuario al grupo docker
sudo usermod -aG docker $USER
# Cerrar sesión y volver a iniciar
```

### Problemas con Volúmenes

**Síntoma:** Cambios en el código no se reflejan en el contenedor.

**Solución:**

1. **Verificar que los volúmenes estén montados correctamente:**
   ```yaml
   volumes:
     - ./app:/app/app
   ```

2. **Reiniciar el contenedor:**
   ```powershell
   docker-compose restart backend
   ```

3. **Para desarrollo, usar modo watch:**
   ```yaml
   command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Comandos Útiles de Diagnóstico

```powershell
# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f backend
docker-compose logs -f frontend

# Ver logs de un contenedor específico
docker logs reservas-backend
docker logs reservas-frontend

# Entrar al contenedor
docker-compose exec backend bash
docker-compose exec backend python

# Ver uso de recursos
docker stats

# Limpiar todo (¡cuidado, elimina todo!)
docker-compose down -v
docker system prune -a
```

## Verificar que Todo Funciona

1. **Backend:**
   ```powershell
   # Verificar health check
   curl http://localhost:8000/health
   # O en navegador: http://localhost:8000/health
   ```

2. **Frontend:**
   - Abre http://localhost:3000 en el navegador

3. **API Docs:**
   - Si DEBUG=True: http://localhost:8000/docs

## Problemas Específicos de Windows

### Docker Desktop no inicia

1. **Verificar WSL 2:**
   ```powershell
   wsl --list --verbose
   ```
   Debe mostrar WSL 2 como versión.

2. **Habilitar características de Windows:**
   - Hyper-V
   - Virtual Machine Platform
   - Windows Subsystem for Linux

3. **Reinstalar Docker Desktop** si es necesario

### Problemas con rutas de Windows

Si tienes problemas con rutas en volúmenes, usa rutas absolutas:

```yaml
volumes:
  - C:/Users/juan4/OneDrive/Escritorio/TFG_DAW/Reservas-de-Citas/app:/app/app
```

O mejor, usa WSL 2 y trabaja desde allí.

## Obtener Ayuda

1. **Logs detallados:**
   ```powershell
   docker-compose logs --tail=100 backend
   ```

2. **Verificar configuración:**
   ```powershell
   docker-compose config
   ```

3. **Probar conexión a Docker:**
   ```powershell
   docker run hello-world
   ```

Si el problema persiste, comparte los logs completos para diagnóstico.

