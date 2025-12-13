# Inicio Rápido - Docker Desktop

## Verificar que Docker Desktop está corriendo

### Método 1: Verificar en la bandeja del sistema
- Busca el ícono de Docker (ballena azul) en la bandeja del sistema (systray)
- Si está ahí, Docker Desktop está corriendo
- Si no está, haz clic derecho en el ícono oculto (^) y busca Docker

### Método 2: Verificar desde PowerShell
```powershell
docker ps
```
Si funciona (muestra una lista, aunque esté vacía), Docker está corriendo.

### Método 3: Abrir Docker Desktop
- Presiona `Win + S` y busca "Docker Desktop"
- Ábrelo desde el menú de inicio
- Espera a que aparezca la ventana de Docker Desktop

## Una vez que Docker Desktop esté corriendo

Ejecuta estos comandos en orden:

```powershell
# 1. Verificar que Docker funciona
docker ps

# 2. Construir las imágenes (primera vez)
docker-compose build

# 3. Levantar los servicios
docker-compose up -d

# 4. Ver los logs
docker-compose logs -f
```

## Si Docker Desktop no inicia

1. **Reiniciar Docker Desktop:**
   - Cierra completamente Docker Desktop desde la bandeja del sistema
   - Vuelve a abrirlo

2. **Verificar WSL 2 (si es necesario):**
   ```powershell
   wsl --list --verbose
   ```
   Debe mostrar al menos una distribución con versión 2.

3. **Reiniciar el equipo** si el problema persiste

## Comandos útiles

```powershell
# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Reiniciar un servicio
docker-compose restart backend
```

## URLs después de iniciar

- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs (si DEBUG=True)

