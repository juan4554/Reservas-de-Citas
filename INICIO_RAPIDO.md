# Inicio Rápido - Docker Desktop

## Verificar que Docker Desktop está corriendo

### Verificar en la bandeja del sistema
- Si lo tienes instalado deberia de estar OK.

### Verificar desde PowerShell

Lanzar el comando **docker ps**

Si funciona (tiene que tener una lista) Docker está corriendo.


## Una vez que Docker Desktop esté corriendo

Ejecuta estos comandos en orden:

# Construir las imágenes
docker-compose build

# Levantar los servicios
docker-compose up -d

# 4. Ver los logs
docker-compose logs -f

## Si Docker Desktop no inicia

1. **Reiniciar Docker Desktop:**
   - Cierra completamente Docker Desktop desde la bandeja del sistema
   - Vuelve a abrirlo

2. **Verificar WSL 2 (si es necesario):**
   
   wsl --list --verbose
   
   Debe mostrar al menos una distribución con versión 2.


## Comandos 


# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener contenedor
docker-compose down

# Reiniciar contenedor
docker-compose restart backend

## URLs después de iniciar

- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Health Check:** http://localhost:8000/health
<img width="454" height="165" alt="image" src="https://github.com/user-attachments/assets/f275cc73-b468-4b37-920a-23c688895d47" />
- **API Docs:** http://localhost:8000/docs

