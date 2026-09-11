# from fastapi import FastAPI
# from routes.user_routes import router

# app = FastAPI(
#     title="device_systems API",
#     description="API REST para la gestión de usuarios del sistema device_systems",
#     version="2.0.0",
#     contact={
#         "name": "Cristian Mesa",
#         "url": "https://github.com/Cristian-Mesa/device_systems",
#     },
# )

# app.include_router(router, tags=["Users"])

from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router

# Crea las tablas en la base de datos si no existen aún
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="API modular con FastAPI, SQLAlchemy y Pydantic v2",
    version="1.0.0"
)

# Conectamos las rutas de usuario
app.include_router(user_router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Device Systems activa y funcionando correctamente"}