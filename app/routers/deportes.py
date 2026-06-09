from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.deporte import Deporte
from app.schemas.deporte import DeporteCreate, DeporteResponse

router = APIRouter(prefix="/api/deportes", tags=["deportes"])

@router.get("/", response_model=list[DeporteResponse])
def listar_deportes(db: Session = Depends(get_db)):
    return db.query(Deporte).all()

@router.post("/", response_model=DeporteResponse)
def crear_deporte(deporte: DeporteCreate, db: Session = Depends(get_db)):
    if db.query(Deporte).filter(Deporte.nombre == deporte.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un deporte con ese nombre")
    nuevo = Deporte(**deporte.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{id}", response_model=DeporteResponse)
def obtener_deporte(id: int, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id == id).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    return deporte

@router.put("/{id}", response_model=DeporteResponse)
def actualizar_deporte(id: int, datos: DeporteCreate, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id == id).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    for key, value in datos.model_dump().items():
        setattr(deporte, key, value)
    db.commit()
    db.refresh(deporte)
    return deporte

@router.delete("/{id}")
def eliminar_deporte(id: int, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id == id).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    db.delete(deporte)
    db.commit()
    return {"mensaje": "Deporte eliminado"}
