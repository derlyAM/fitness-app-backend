from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, deportes, ejercicios, rutinas, sesiones

import app.models.usuario
import app.models.deporte
import app.models.ejercicio
import app.models.rutina
import app.models.rutina_ejercicio
import app.models.sesion
import app.models.sesion_ejercicio

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness App API",
    description="Backend para registro de actividad física y rutinas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(deportes.router)
app.include_router(ejercicios.router)
app.include_router(rutinas.router)
app.include_router(sesiones.router)

@app.get("/")
def root():
    return {"mensaje": "Fitness App API corriendo"}
