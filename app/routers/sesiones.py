from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.sesion import Sesion
from app.models.rutina import Rutina
from app.schemas.sesion import SesionCreate, SesionResponse
from app.routers.auth import get_current_user_id

router = APIRouter(prefix="/api/sesiones", tags=["sesiones"])

@router.get("/", response_model=list[SesionResponse])
def listar_sesiones(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    sesiones = db.query(Sesion).options(
        joinedload(Sesion.rutina).joinedload(Rutina.deporte)
    ).filter(Sesion.usuario_id == usuario_id).all()
    result = []
    for s in sesiones:
        nombre_deporte = s.rutina.deporte.nombre if s.rutina and s.rutina.deporte else None
        result.append(SesionResponse(
            id=s.id,
            fecha=s.fecha,
            usuario_id=s.usuario_id,
            rutina_id=s.rutina_id,
            duracion=s.duracion,
            notas=s.notas,
            nombre_deporte=nombre_deporte,
        ))
    return result

@router.get("/deporte/{deporte_id}", response_model=list[SesionResponse])
def sesiones_por_deporte(
    deporte_id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    return db.query(Sesion)\
        .join(Rutina)\
        .filter(Rutina.deporte_id == deporte_id, Sesion.usuario_id == usuario_id)\
        .all()

@router.get("/{id}", response_model=SesionResponse)
def obtener_sesion(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    sesion = db.query(Sesion).filter(Sesion.id == id, Sesion.usuario_id == usuario_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sesion

@router.post("/", response_model=SesionResponse)
def crear_sesion(
    sesion: SesionCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    nueva = Sesion(**sesion.model_dump(), usuario_id=usuario_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id}", response_model=SesionResponse)
def actualizar_sesion(
    id: int,
    datos: SesionCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    sesion = db.query(Sesion).filter(Sesion.id == id, Sesion.usuario_id == usuario_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    for key, value in datos.model_dump().items():
        setattr(sesion, key, value)
    db.commit()
    db.refresh(sesion)
    return sesion

@router.delete("/{id}")
def eliminar_sesion(
    id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    sesion = db.query(Sesion).filter(Sesion.id == id, Sesion.usuario_id == usuario_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    db.delete(sesion)
    db.commit()
    return {"mensaje": "Sesión eliminada"}
