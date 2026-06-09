from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Sesion(Base):
    __tablename__ = "sesiones"

    id         = Column(Integer, primary_key=True, index=True)
    fecha      = Column(DateTime, default=datetime.utcnow)
    duracion   = Column(Integer, nullable=True)
    notas      = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    rutina_id  = Column(Integer, ForeignKey("rutinas.id"))

    usuario           = relationship("Usuario", back_populates="sesiones")
    rutina            = relationship("Rutina",  back_populates="sesiones")
    sesion_ejercicios = relationship("SesionEjercicio", back_populates="sesion", cascade="all, delete-orphan")
