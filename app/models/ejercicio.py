from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ejercicio(Base):
    __tablename__ = "ejercicios"

    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String, nullable=False)
    grupo_muscular = Column(String, nullable=True)
    descripcion    = Column(String, nullable=True)
    deporte_id     = Column(Integer, ForeignKey("deportes.id"))

    deporte           = relationship("Deporte", back_populates="ejercicios")
    rutina_ejercicios = relationship("RutinaEjercicio", back_populates="ejercicio")
    sesion_ejercicios = relationship("SesionEjercicio", back_populates="ejercicio")
