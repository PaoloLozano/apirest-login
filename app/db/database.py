from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# URL DE BASE DE DATOS
# =========================
from app.core.config import DATABASE_URL
# =========================
# CONEXION
# =========================
engine = create_engine(DATABASE_URL)

# =========================
# SESIONES
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE DE MODELOS
# =========================
Base = declarative_base()

# =========================
# DEPENDENCIA (FastAPI)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
