from pydantic import BaseModel

class RutinaEjercicioBase(BaseModel):
    ejercicio_id: int
    series: int | None = None
    repeticiones: int | None = None

class RutinaEjercicioCreate(RutinaEjercicioBase):
    rutina_id: int

class RutinaEjercicioResponse(RutinaEjercicioBase):
    id: int
    rutina_id: int

    class Config:
        from_attributes = True
