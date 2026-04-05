from fastapi import FastAPI
from app.routers import user_router

app = FastAPI()

app.include_router(user_router.router)
@app.get("/")
def inicio(): 
    return {"mensaje": "API funcionando"} 