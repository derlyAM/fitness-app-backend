from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Deporte(Base):
    __tablename__ = "deportes"

    id     = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    icono  = Column(String, nullable=True)

    rutinas    = relationship("Rutina",    back_populates="deporte", cascade="all, delete-orphan")
    ejercicios = relationship("Ejercicio", back_populates="deporte", cascade="all, delete-orphan")
