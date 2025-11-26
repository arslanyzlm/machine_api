from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import (
    departments,
    machines,
    status_types,
    status_history,
    department_leaders,
    machine_operators,
    profiles,
    auth,
)
# Eğer tablolar zaten PostgreSQL'de varsa, buradaki create_all'ı kapatabilirsin
# ama şimdilik zarar vermez, eşleşen tabloları zorlamaz.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Machine Status API")

# CORS (React'in bağlanabilmesi için)
origins = [
    "http://localhost:5173",  # Vite ise
    "http://localhost:3000",  # Create React App ise
    "http://arslan",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departments.router)
app.include_router(machines.router)
app.include_router(status_types.router)
app.include_router(status_history.router)
app.include_router(department_leaders.router)
app.include_router(machine_operators.router)
app.include_router(profiles.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Machine Status API is running"}
