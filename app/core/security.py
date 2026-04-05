from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user_model import UsuarioDB

# ========================
# CONFIG JWT
# ========================
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# ========================
# HASH PASSWORD
# ========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

# ========================
# TOKEN
# ========================
def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ========================
# OAUTH2
# ========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ========================
# USUARIO ACTUAL
# ========================
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre = payload.get("sub")

        if nombre is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(UsuarioDB).filter(UsuarioDB.nombre == nombre).first()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return usuario

# ========================
# SOLO ADMIN
# ========================
def solo_admin(usuario: UsuarioDB = Depends(obtener_usuario_actual)):
    # Verificar el rol del usuario (elimina espacios y compara en minúsculas)
    rol_normalizado = usuario.rol.strip().lower() if usuario.rol else ""
    if rol_normalizado != "admin":
        raise HTTPException(
            status_code=403,
            detail=f"No tienes permisos. Tu rol actual es: '{usuario.rol}'"
        )
    return usuario