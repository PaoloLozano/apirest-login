from fastapi import FastAPI
from app.routers import user_router
from app.db.database import engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Crea las tablas al iniciar si no existen"""
    logger.info("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas/verificadas exitosamente")

app.include_router(user_router.router)

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando", "base_datos": "conectada"} 