from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.auth import router as auth_router
from app.api.routers.facilities import router as facilities_router
from app.api.routers.slots import router as slots_router
from app.api.routers.admin_users import router as admin_users_router
from app.api.routers.admin_reservations import router as admin_reservations_router




app = FastAPI(title="Reserva Sport", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(facilities_router)
app.include_router(slots_router)
app.include_router(admin_users_router)
app.include_router(admin_reservations_router)

@app.get("/health")
def health():
    return {"status": "ok"}


