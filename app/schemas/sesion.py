from pydantic import BaseModel
from datetime import datetime

class SesionBase(BaseModel):
    duracion: int | None = None
    notas: str | None = None
    rutina_id: int

class SesionCreate(SesionBase):
    pass

class SesionResponse(SesionBase):
    id: int
    fecha: datetime
    usuario_id: int
    nombre_deporte: str | None = None

    class Config:
        from_attributes = True
