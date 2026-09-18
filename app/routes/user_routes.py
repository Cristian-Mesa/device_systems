# from fastapi import APIRouter, Depends
# from schemas.user_schema import UserCreate, UserUpdate, User, UserRole
# from services import user_service
# from dependencies.user_dependencies import (
#     get_user_or_404,
#     agregar_cabeceras_app,
#     validar_correo_no_duplicado,
#     validar_correo_no_duplicado_en_actualizacion,
#     validar_rol_permitido,
#     verificar_token_simulado,
# )

# router = APIRouter(dependencies=[Depends(agregar_cabeceras_app)])


# @router.get(
#     "/users",
#     response_model=list[User],
#     summary="Listar usuarios",
#     description="Devuelve la lista completa de usuarios. Permite filtrar por rol y por estado activo mediante query parameters.",
#     response_description="Lista de usuarios encontrados",
# )
# def listar_usuarios(role: UserRole = Depends(validar_rol_permitido), is_active: bool = None):
#     return user_service.listar_usuarios(role, is_active)


# @router.get(
#     "/users/{user_id}",
#     response_model=User,
#     summary="Obtener usuario por id",
#     description="Consulta un usuario específico según su identificador. Responde 404 si el usuario no existe.",
#     response_description="Usuario encontrado",
# )
# def obtener_usuario(usuario: dict = Depends(get_user_or_404)):
#     return usuario


# @router.post(
#     "/users",
#     response_model=User,
#     status_code=201,
#     summary="Crear usuario",
#     description="Registra un nuevo usuario. Valida los datos de entrada con Pydantic y evita correos duplicados. Requiere la cabecera X-API-Key.",
#     response_description="Usuario creado",
#     dependencies=[Depends(verificar_token_simulado)],
# )
# def crear_usuario(user: UserCreate = Depends(validar_correo_no_duplicado)):
#     return user_service.crear_usuario(user)


# @router.put(
#     "/users/{user_id}",
#     response_model=User,
#     summary="Actualizar usuario completo",
#     description="Reemplaza todos los campos de un usuario existente. Requiere enviar todos los campos obligatorios y la cabecera X-API-Key. Responde 404 si el usuario no existe.",
#     response_description="Usuario actualizado",
#     dependencies=[Depends(verificar_token_simulado)],
# )
# def actualizar_usuario_completo(
#     user_update: UserCreate,
#     usuario: dict = Depends(validar_correo_no_duplicado_en_actualizacion),
# ):
#     return user_service.actualizar_usuario_completo(usuario["id"], user_update)


# @router.patch(
#     "/users/{user_id}",
#     response_model=User,
#     summary="Actualizar usuario parcialmente",
#     description="Modifica solo los campos enviados por el cliente. Requiere la cabecera X-API-Key. Responde 400 si no se envía ningún campo, y 404 si el usuario no existe.",
#     response_description="Usuario actualizado parcialmente",
#     dependencies=[Depends(verificar_token_simulado)],
# )
# def actualizar_usuario_parcial(user_update: UserUpdate, usuario: dict = Depends(get_user_or_404)):
#     return user_service.actualizar_usuario_parcial(usuario["id"], user_update)


# @router.delete(
#     "/users/{user_id}",
#     summary="Eliminar usuario",
#     description="Elimina un usuario existente del sistema. Requiere la cabecera X-API-Key. Responde 404 si el usuario no existe.",
#     response_description="Confirmación de eliminación",
#     dependencies=[Depends(verificar_token_simulado)],
# )
# def eliminar_usuario(usuario: dict = Depends(get_user_or_404)):
#     return user_service.eliminar_usuario(usuario["id"])

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, Userpatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import loan_service, user_service

router = APIRouter(prefix="/users", tags=["Users"])

# 1. LISTAR USUARIOS (con filtros y ordenamiento)
@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query("created_at", description="Ordenar por 'name' o 'created_at'"),
    db: Session = Depends(get_db)
):
    return user_service.listar_usuarios(db, role=role, is_active=is_active, order_by=order_by)

# 2. OBTENER USUARIO POR ID
@router.get("/{usuario_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = user_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return usuario

# 3. CREAR USUARIO
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario_data: UserCreate, db: Session = Depends(get_db)):
    if user_service.obtener_usuario_por_email(db, usuario_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya está registrado"
        )
    return user_service.crear_usuario(db, usuario_data)

# 4. ACTUALIZACIÓN COMPLETA (PUT)
@router.put("/{usuario_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def actualizar_usuario_completo(usuario_id: int, usuario_data: UserUpdate, db: Session = Depends(get_db)):
    usuario = user_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    # Validar que si cambia el email, no pertenezca a otro usuario
    usuario_existente = user_service.obtener_usuario_por_email(db, usuario_data.email)
    if usuario_existente and usuario_existente.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya pertenece a otro usuario"
        )
        
    return user_service.actualizar_usuario_completo(db, usuario, usuario_data)

# 5. ACTUALIZACIÓN PARCIAL (PATCH)
@router.patch("/{usuario_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def actualizar_usuario_parcial(usuario_id: int, usuario_data: Userpatch, db: Session = Depends(get_db)):
    usuario = user_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    if usuario_data.email:
        usuario_existente = user_service.obtener_usuario_por_email(db, usuario_data.email)
        if usuario_existente and usuario_existente.id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El email ya pertenece a otro usuario"
            )

    return user_service.actualizar_usuario_parcial(db, usuario, usuario_data)

# 6. ELIMINAR USUARIO
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = user_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    if loan_service.list_loans_for_user(db, usuario_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un usuario con prestamos registrados",
        )
    user_service.eliminar_usuario(db, usuario)
    return None

@router.get("/{usuario_id}/loans", response_model=List[LoanDetailResponse], summary="Prestamos de un usuario")
def obtener_prestamos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = user_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return loan_service.list_loans_for_user(db, usuario_id)
