from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ejercicio import Ejercicio
from app.schemas.ejercicio import EjercicioCreate, EjercicioResponse

router = APIRouter(prefix="/api/ejercicios", tags=["ejercicios"])

@router.get("/", response_model=list[EjercicioResponse])
def listar_ejercicios(db: Session = Depends(get_db)):
    return db.query(Ejercicio).all()

@router.get("/deporte/{deporte_id}", response_model=list[EjercicioResponse])
def ejercicios_por_deporte(deporte_id: int, db: Session = Depends(get_db)):
    return db.query(Ejercicio).filter(Ejercicio.deporte_id == deporte_id).all()

@router.post("/", response_model=EjercicioResponse)
def crear_ejercicio(ejercicio: EjercicioCreate, db: Session = Depends(get_db)):
    nuevo = Ejercicio(**ejercicio.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id}", response_model=EjercicioResponse)
def actualizar_ejercicio(id: int, datos: EjercicioCreate, db: Session = Depends(get_db)):
    ejercicio = db.query(Ejercicio).filter(Ejercicio.id == id).first()
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    for key, value in datos.model_dump().items():
        setattr(ejercicio, key, value)
    db.commit()
    db.refresh(ejercicio)
    return ejercicio

@router.delete("/{id}")
def eliminar_ejercicio(id: int, db: Session = Depends(get_db)):
    ejercicio = db.query(Ejercicio).filter(Ejercicio.id == id).first()
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    db.delete(ejercicio)
    db.commit()
    return {"mensaje": "Ejercicio eliminado"}
