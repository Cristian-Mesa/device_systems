from fastapi import HTTPException
from data.users_db import fake_users_db
from schemas.user_schema import UserCreate, UserUpdate, User, UserRole


def listar_usuarios(role: UserRole = None, is_active: bool = None):
    resultado = fake_users_db
    if role is not None:
        resultado = [user for user in resultado if user["role"] == role]
    if is_active is not None:
        resultado = [user for user in resultado if user["is_active"] == is_active]
    return resultado


def obtener_usuario_por_id(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


def existe_email_duplicado(email: str, excluir_id: int = None) -> bool:
    for user in fake_users_db:
        if user["email"] == email and user["id"] != excluir_id:
            return True
    return False


def crear_usuario(user: UserCreate):
    if existe_email_duplicado(user.email):
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

    new_user = user.model_dump()

    if fake_users_db:
        nuevo_id = max(u["id"] for u in fake_users_db) + 1
    else:
        nuevo_id = 1
    new_user["id"] = nuevo_id
    fake_users_db.append(new_user)
    return new_user


def actualizar_usuario_parcial(user_id: int, user_update: UserUpdate):
    usuario = obtener_usuario_por_id(user_id)

    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    if "email" in update_data and existe_email_duplicado(update_data["email"], excluir_id=user_id):
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

    usuario.update(update_data)
    return usuario


def actualizar_usuario_completo(user_id: int, user_update: UserCreate):
    usuario = obtener_usuario_por_id(user_id)

    if existe_email_duplicado(user_update.email, excluir_id=user_id):
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

    update_data = user_update.model_dump()
    usuario.update(update_data)
    return usuario


def eliminar_usuario(user_id: int):
    usuario = obtener_usuario_por_id(user_id)
    fake_users_db.remove(usuario)
    return {"detail": "Usuario eliminado correctamente"}
