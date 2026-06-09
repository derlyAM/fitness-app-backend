from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Rutina(Base):
    __tablename__ = "rutinas"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    deporte_id  = Column(Integer, ForeignKey("deportes.id"))
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"))

    deporte           = relationship("Deporte", back_populates="rutinas")
    rutina_ejercicios = relationship("RutinaEjercicio", back_populates="rutina", cascade="all, delete-orphan")
    sesiones          = relationship("Sesion",          back_populates="rutina", cascade="all, delete-orphan")
