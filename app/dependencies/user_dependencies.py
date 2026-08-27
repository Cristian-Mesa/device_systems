from fastapi import Depends, Header, HTTPException, Response
from schemas.user_schema import UserCreate, UserRole
from services import user_service

TOKEN_ESPERADO = "device_systems_key"


def get_user_or_404(user_id: int):
    return user_service.obtener_usuario_por_id(user_id)


def validar_correo_no_duplicado(user: UserCreate):
    if user_service.existe_email_duplicado(user.email):
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")
    return user


def validar_correo_no_duplicado_en_actualizacion(
    user_update: UserCreate, usuario: dict = Depends(get_user_or_404)
):
    if user_service.existe_email_duplicado(user_update.email, excluir_id=usuario["id"]):
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")
    return usuario


def validar_rol_permitido(role: UserRole = None):
    return role


def obtener_configuracion_api():
    return {"app_name": "device_systems", "api_version": "1.0"}


def agregar_cabeceras_app(response: Response, config: dict = Depends(obtener_configuracion_api)):
    response.headers["X-App-Name"] = config["app_name"]
    response.headers["X-API-Version"] = config["api_version"]


def verificar_token_simulado(x_api_key: str = Header(default=None)):
    if x_api_key != TOKEN_ESPERADO:
        raise HTTPException(status_code=401, detail="Token de autenticación inválido o ausente")
