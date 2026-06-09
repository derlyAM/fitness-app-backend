from pydantic import BaseModel

class RutinaBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    deporte_id: int

class RutinaCreate(RutinaBase):
    pass

class RutinaResponse(RutinaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True
