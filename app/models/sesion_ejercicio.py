from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SesionEjercicio(Base):
    __tablename__ = "sesion_ejercicios"

    id            = Column(Integer, primary_key=True, index=True)
    sesion_id     = Column(Integer, ForeignKey("sesiones.id"))
    ejercicio_id  = Column(Integer, ForeignKey("ejercicios.id"))
    series_hechas = Column(Integer, nullable=True)
    reps_hechas   = Column(Integer, nullable=True)
    peso_kg       = Column(Float, nullable=True)

    sesion    = relationship("Sesion", back_populates="sesion_ejercicios")
    ejercicio = relationship("Ejercicio", back_populates="sesion_ejercicios")
