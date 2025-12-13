.PHONY: help install test test-cov run docker-up docker-down docker-build migrate

help:
	@echo "Comandos disponibles:"
	@echo "  make install      - Instalar dependencias"
	@echo "  make test         - Ejecutar tests"
	@echo "  make test-cov     - Ejecutar tests con cobertura"
	@echo "  make run          - Ejecutar servidor de desarrollo"
	@echo "  make docker-up    - Levantar contenedores Docker"
	@echo "  make docker-down  - Detener contenedores Docker"
	@echo "  make docker-build - Construir imágenes Docker"
	@echo "  make migrate      - Ejecutar migraciones"

install:
	pip install -r requirements.txt

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

migrate:
	alembic upgrade head

