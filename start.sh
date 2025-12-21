#!/bin/bash

# Script de inicio rápido para desarrollo

echo "Iniciando Reservas de Citas..."

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "Archivo .env no encontrado. Creando desde .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Archivo .env creado. Por favor, edítalo con tus configuraciones."
    else
        echo ".env.example no encontrado. Creando .env básico..."
        cat > .env << EOF
DATABASE_URL=sqlite:///./reserva.db
JWT_SECRET=change-this-secret-key-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
EOF
    fi
fi

# Verificar si existe venv
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Verificar base de datos
if [ ! -f "reserva.db" ]; then
    echo "Base de datos no encontrada. Ejecutando migraciones..."
    alembic upgrade head
fi

echo "Todo listo!"
echo ""
echo "Para iniciar el servidor:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Para ejecutar tests:"
echo "  pytest"
echo ""
echo "Para usar Docker:"
echo "  docker-compose up -d"
echo ""

