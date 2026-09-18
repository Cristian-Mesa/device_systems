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
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.user_routes import router as user_router

# Crea las tablas en la base de datos si no existen aún

app = FastAPI(
    title="Device Systems API",
    description="API para gestionar usuarios, dispositivos y prestamos.",
    version="2.0.0"
)

# Conectamos las rutas de usuario
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Device Systems activa y funcionando correctamente"}