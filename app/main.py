from fastapi import FastAPI
from routes.user_routes import router 
app = FastAPI(title="device_systems")

app.include_router(router)
