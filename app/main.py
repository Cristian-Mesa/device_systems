import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.auth.auth_routes import router as auth_router
from app.middlewares.request_middleware import add_request_information
from app.rate_limit import limiter
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.user_routes import router as user_router


load_dotenv()

allowed_origins = os.getenv(
    'CORS_ORIGINS',
    'http://localhost:5173,http://localhost:3000',
).split(',')

app = FastAPI(
    title='Device Systems API',
    description='API REST segura para gestionar usuarios, dispositivos y prestamos.',
    version='3.0.0',
    openapi_tags=[
        {'name': 'Auth', 'description': 'Registro e inicio de sesion.'},
        {'name': 'Users', 'description': 'Gestion de usuarios.'},
        {'name': 'Devices', 'description': 'Gestion de dispositivos.'},
        {'name': 'Loans', 'description': 'Gestion de prestamos.'},
        {'name': 'Security', 'description': 'Rutas que requieren token.'},
    ],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.middleware('http')
async def request_middleware(request, call_next):
    return await add_request_information(request, call_next)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(auth_router)


@app.get('/', tags=['Root'])
def root():
    return {'message': 'API de Device Systems activa y funcionando correctamente'}