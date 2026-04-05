# user_schema.py
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=50)
    edad: int = Field(gt=0, lt=150)
    email: EmailStr
    password: str
    rol: str = "user"
    dni: str = Field(min_length=8, max_length=8, description="DNI del usuario, 8 caracteres")

    # VALIDACIÓN PERSONALIZADA
    @field_validator("edad")
    def validar_edad(cls, value):
        if value < 18:
            raise ValueError("Debes ser mayor de edad")
        return value

    @field_validator("password")
    def validar_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password muy corto")
        if not any(char.isdigit() for char in value):
            raise ValueError("Debe tener al menos un número")
        if not any(char.isupper() for char in value):
            raise ValueError("Debe tener una mayúscula")
        return value

    @field_validator("rol")
    def validar_rol(cls, value):
        if value not in ["admin", "user"]:
            raise ValueError("Rol inválido")
        return value

    @field_validator("nombre")
    def validar_nombre(cls, value):
        return value.lower()  # lowercase para evitar problemas de mayúsculas en el login

    @field_validator("dni")
    def validar_dni(cls, value):
        if not value.isdigit():
            raise ValueError("El DNI debe contener solo números")
        return value


class UsuarioResponse(BaseModel):
    """Schema para retornar datos de usuario (sin password)"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    edad: int
    email: str
    rol: str
    dni: str | None = None 