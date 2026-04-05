import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONFIGURACION BASE DE DATOS
# Render usa DATABASE_URL externo
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

# Solo usar SQLite si no hay DATABASE_URL (desarrollo local)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./app.db"

# =========================
# SEGURIDAD
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-por-defecto-cambiar-en-produccion")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
