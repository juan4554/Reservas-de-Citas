import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routers.auth import router as auth_router
from app.api.routers.facilities import router as facilities_router
from app.api.routers.slots import router as slots_router
from app.api.routers.admin_users import router as admin_users_router
from app.api.routers.admin_reservations import router as admin_reservations_router
from app.api.routers.reservations import router as reservations_router

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info("Starting up Reserva Sport API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database_url}")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Reserva Sport",
    version="0.1.0",
    description="API para gestión de reservas de instalaciones deportivas",
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

# Configurar CORS de forma segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(facilities_router)
app.include_router(slots_router)
app.include_router(reservations_router)
app.include_router(admin_users_router)
app.include_router(admin_reservations_router)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": "0.1.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error" if not settings.debug else str(exc)
        }
    )


