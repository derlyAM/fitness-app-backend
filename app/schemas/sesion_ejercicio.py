from pydantic import BaseModel

class SesionEjercicioBase(BaseModel):
    ejercicio_id: int
    series_hechas: int | None = None
    reps_hechas: int | None = None
    peso_kg: float | None = None

class SesionEjercicioCreate(SesionEjercicioBase):
    sesion_id: int

class SesionEjercicioResponse(SesionEjercicioBase):
    id: int
    sesion_id: int

    class Config:
        from_attributes = True
