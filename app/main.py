from fastapi import FastAPI
from routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="2.0.0",
    contact={
        "name": "Cristian Mesa",
        "url": "https://github.com/Cristian-Mesa/device_systems",
    },
)

app.include_router(router, tags=["Users"])
