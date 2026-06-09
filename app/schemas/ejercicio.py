from pydantic import BaseModel

class EjercicioBase(BaseModel):
    nombre: str
    grupo_muscular: str | None = None
    descripcion: str | None = None
    deporte_id: int

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioResponse(EjercicioBase):
    id: int

    class Config:
        from_attributes = True
