# from fastapi import HTTPException
# from data.users_db import fake_users_db
# from schemas.user_schema import UserCreate, UserUpdate, User, UserRole


# def listar_usuarios(role: UserRole = None, is_active: bool = None):
#     resultado = fake_users_db
#     if role is not None:
#         resultado = [user for user in resultado if user["role"] == role]
#     if is_active is not None:
#         resultado = [user for user in resultado if user["is_active"] == is_active]
#     return resultado


# def obtener_usuario_por_id(user_id: int):
#     for user in fake_users_db:
#         if user["id"] == user_id:
#             return user
#     raise HTTPException(status_code=404, detail="Usuario no encontrado")


# def existe_email_duplicado(email: str, excluir_id: int = None) -> bool:
#     for user in fake_users_db:
#         if user["email"] == email and user["id"] != excluir_id:
#             return True
#     return False


# def crear_usuario(user: UserCreate):
#     if existe_email_duplicado(user.email):
#         raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

#     new_user = user.model_dump()

#     if fake_users_db:
#         nuevo_id = max(u["id"] for u in fake_users_db) + 1
#     else:
#         nuevo_id = 1
#     new_user["id"] = nuevo_id
#     fake_users_db.append(new_user)
#     return new_user


# def actualizar_usuario_parcial(user_id: int, user_update: UserUpdate):
#     usuario = obtener_usuario_por_id(user_id)

#     update_data = user_update.model_dump(exclude_unset=True)
#     if not update_data:
#         raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

#     if "email" in update_data and existe_email_duplicado(update_data["email"], excluir_id=user_id):
#         raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

#     usuario.update(update_data)
#     return usuario


# def actualizar_usuario_completo(user_id: int, user_update: UserCreate):
#     usuario = obtener_usuario_por_id(user_id)

#     if existe_email_duplicado(user_update.email, excluir_id=user_id):
#         raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

#     update_data = user_update.model_dump()
#     usuario.update(update_data)
#     return usuario


# def eliminar_usuario(user_id: int):
#     usuario = obtener_usuario_por_id(user_id)
#     fake_users_db.remove(usuario)
#     return {"detail": "Usuario eliminado correctamente"}

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, Userpatch


def crear_usuario(db: Session, usuario_data: UserCreate) -> User:
    db_usuario = User(**usuario_data.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario_por_id(db: Session, usuario_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == usuario_id).first()

def obtener_usuario_por_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def listar_usuarios(
    db: Session, 
    role: Optional[str] = None, 
    is_active: Optional[bool] = None,
    order_by: Optional[str] = "created_at"
) -> List[User]:
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if order_by == "name":
        query = query.order_by(User.name.asc())
    else:
        query = query.order_by(User.created_at.desc())
        
    return query.all()


def actualizar_usuario_completo(db: Session, db_usuario: User, usuario_data: UserUpdate) -> User:
    for key, value in usuario_data.model_dump().items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def actualizar_usuario_parcial(db: Session, db_usuario: User, usuario_data: Userpatch) -> User:
    # exclude_unset=True ignora los campos no enviados en la petición
    datos = usuario_data.model_dump(exclude_unset=True)
    for key, value in datos.items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def eliminar_usuario(db: Session, db_usuario: User) -> None:
    db.delete(db_usuario)
    db.commit()