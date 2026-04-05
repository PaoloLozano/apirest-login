from sqlalchemy import Column, Integer, String
from app.db.database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    edad = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)
    rol = Column(String, default="user") 
    dni = Column(String, nullable=True)