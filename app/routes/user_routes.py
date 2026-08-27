from fastapi import APIRouter, Depends
from schemas.user_schema import UserCreate, UserUpdate, User, UserRole
from services import user_service
from dependencies.user_dependencies import (
    get_user_or_404,
    agregar_cabeceras_app,
    validar_correo_no_duplicado,
    validar_correo_no_duplicado_en_actualizacion,
    validar_rol_permitido,
    verificar_token_simulado,
)

router = APIRouter(dependencies=[Depends(agregar_cabeceras_app)])


@router.get(
    "/users",
    response_model=list[User],
    summary="Listar usuarios",
    description="Devuelve la lista completa de usuarios. Permite filtrar por rol y por estado activo mediante query parameters.",
    response_description="Lista de usuarios encontrados",
)
def listar_usuarios(role: UserRole = Depends(validar_rol_permitido), is_active: bool = None):
    return user_service.listar_usuarios(role, is_active)


@router.get(
    "/users/{user_id}",
    response_model=User,
    summary="Obtener usuario por id",
    description="Consulta un usuario específico según su identificador. Responde 404 si el usuario no existe.",
    response_description="Usuario encontrado",
)
def obtener_usuario(usuario: dict = Depends(get_user_or_404)):
    return usuario


@router.post(
    "/users",
    response_model=User,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida los datos de entrada con Pydantic y evita correos duplicados. Requiere la cabecera X-API-Key.",
    response_description="Usuario creado",
    dependencies=[Depends(verificar_token_simulado)],
)
def crear_usuario(user: UserCreate = Depends(validar_correo_no_duplicado)):
    return user_service.crear_usuario(user)


@router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los campos de un usuario existente. Requiere enviar todos los campos obligatorios y la cabecera X-API-Key. Responde 404 si el usuario no existe.",
    response_description="Usuario actualizado",
    dependencies=[Depends(verificar_token_simulado)],
)
def actualizar_usuario_completo(
    user_update: UserCreate,
    usuario: dict = Depends(validar_correo_no_duplicado_en_actualizacion),
):
    return user_service.actualizar_usuario_completo(usuario["id"], user_update)


@router.patch(
    "/users/{user_id}",
    response_model=User,
    summary="Actualizar usuario parcialmente",
    description="Modifica solo los campos enviados por el cliente. Requiere la cabecera X-API-Key. Responde 400 si no se envía ningún campo, y 404 si el usuario no existe.",
    response_description="Usuario actualizado parcialmente",
    dependencies=[Depends(verificar_token_simulado)],
)
def actualizar_usuario_parcial(user_update: UserUpdate, usuario: dict = Depends(get_user_or_404)):
    return user_service.actualizar_usuario_parcial(usuario["id"], user_update)


@router.delete(
    "/users/{user_id}",
    summary="Eliminar usuario",
    description="Elimina un usuario existente del sistema. Requiere la cabecera X-API-Key. Responde 404 si el usuario no existe.",
    response_description="Confirmación de eliminación",
    dependencies=[Depends(verificar_token_simulado)],
)
def eliminar_usuario(usuario: dict = Depends(get_user_or_404)):
    return user_service.eliminar_usuario(usuario["id"])
