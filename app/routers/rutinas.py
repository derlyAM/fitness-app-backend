from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rutina import Rutina
from app.schemas.rutina import RutinaCreate, RutinaResponse
from app.routers.auth import get_current_user_id

router = APIRouter(prefix="/api/rutinas", tags=["rutinas"])

@router.get("/", response_model=list[RutinaResponse])
def listar_rutinas(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    return db.query(Rutina).filter(Rutina.usuario_id == usuario_id).all()

@router.get("/{id}", response_model=RutinaResponse)
def obtener_rutina(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    rutina = db.query(Rutina).filter(Rutina.id == id, Rutina.usuario_id == usuario_id).first()
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return rutina

@router.post("/", response_model=RutinaResponse)
def crear_rutina(
    rutina: RutinaCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    nueva = Rutina(**rutina.model_dump(), usuario_id=usuario_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id}", response_model=RutinaResponse)
def actualizar_rutina(
    id: int,
    datos: RutinaCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    rutina = db.query(Rutina).filter(Rutina.id == id, Rutina.usuario_id == usuario_id).first()
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    for key, value in datos.model_dump().items():
        setattr(rutina, key, value)
    db.commit()
    db.refresh(rutina)
    return rutina

@router.delete("/{id}")
def eliminar_rutina(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    rutina = db.query(Rutina).filter(Rutina.id == id, Rutina.usuario_id == usuario_id).first()
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    db.delete(rutina)
    db.commit()
    return {"mensaje": "Rutina eliminada"}
