from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services import user_service
from app.core.security import solo_admin, obtener_usuario_actual, crear_token
from app.schemas.user_schema import UsuarioCreate, UsuarioResponse

router = APIRouter()

@router.post("/registro")
def registro(
    nombre: str = Form(..., min_length=3, max_length=50, description="Nombre del usuario (mínimo 3 caracteres)"),
    edad: int = Form(..., gt=0, lt=150, description="Edad (debe ser mayor de 18)"),
    email: str = Form(..., description="Email válido"),
    password: str = Form(..., description="Password (mínimo 8 caracteres, 1 mayúscula, 1 número)"),
    rol: str = Form("user", description="Rol: admin o user"),
    dni: str = Form(..., min_length=8, max_length=8, description="DNI del usuario, 8 caracteres"),
    db: Session = Depends(get_db)
):
    # Validar manualmente usando el schema
    from pydantic import ValidationError
    try:
        usuario = UsuarioCreate(
            nombre=nombre,
            edad=edad,
            email=email,
            password=password,
            rol=rol,
            dni=dni
        )
    except ValidationError as e:
        # Extraer los errores de validación con mensajes específicos
        errores = []
        for error in e.errors():
            errores.append({
                "campo": error.get("loc", ["unknown"])[-1],
                "mensaje": error.get("msg")
            })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Error de validación",
                "detalles": errores
            }
        )

    nuevo_usuario = user_service.crear_usuario(db, usuario.nombre, usuario.edad, usuario.email, usuario.password, usuario.rol, usuario.dni)
    return {
        "mensaje": f"Se ha registrado usuario {nuevo_usuario.nombre} exitosamente",
        "usuario": {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "edad": nuevo_usuario.edad,
            "email": nuevo_usuario.email,
            "rol": nuevo_usuario.rol,
            "dni": nuevo_usuario.dni
        }
    }

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = user_service.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre o contraseña incorrectos"
        )
    token = crear_token(data={"sub": usuario.nombre})
    return {
        "access_token": token,
        "token_type": "bearer",
        "mensaje": f"Bienvenido {usuario.nombre}"
    }

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar(admin=Depends(solo_admin), db: Session = Depends(get_db)):
    usuarios = user_service.obtener_usuarios(db)
    return usuarios

@router.get("/perfil", response_model=UsuarioResponse)
def perfil(usuario=Depends(obtener_usuario_actual)):
    return usuario 