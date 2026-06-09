from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class RutinaEjercicio(Base):
    __tablename__ = "rutina_ejercicios"

    id           = Column(Integer, primary_key=True, index=True)
    rutina_id    = Column(Integer, ForeignKey("rutinas.id"))
    ejercicio_id = Column(Integer, ForeignKey("ejercicios.id"))
    series       = Column(Integer, nullable=True)
    repeticiones = Column(Integer, nullable=True)

    rutina    = relationship("Rutina", back_populates="rutina_ejercicios")
    ejercicio = relationship("Ejercicio", back_populates="rutina_ejercicios")
