from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import UsuarioDB
from app.core.security import hash_password, verify_password

def autenticar_usuario(db: Session, nombre: str, password: str):
    """Autentica un usuario por nombre y contraseña"""
    usuario = db.query(UsuarioDB).filter(UsuarioDB.nombre == nombre).first()
    if not usuario:
        return None
    if not verify_password(password, usuario.password):
        return None
    return usuario

def crear_usuario(db, nombre, edad, email, password, rol, dni):
    existe = db.query(UsuarioDB).filter(UsuarioDB.nombre == nombre).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    # VALIDACIÓN DE NEGOCIO
    if rol not in ["admin", "user"]:
        raise HTTPException(
            status_code=400,
            detail="Rol inválido"
        )

    nuevo = UsuarioDB(
        nombre=nombre,
        edad=edad,
        email=email,
        password=hash_password(password),
        rol=rol,
        dni=dni
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

def obtener_usuarios(db: Session):
    """Obtiene todos los usuarios"""
    return db.query(UsuarioDB).all()  