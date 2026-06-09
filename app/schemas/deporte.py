from pydantic import BaseModel

class DeporteBase(BaseModel):
    nombre: str
    icono: str | None = None

class DeporteCreate(DeporteBase):
    pass

class DeporteResponse(DeporteBase):
    id: int

    class Config:
        from_attributes = True
