from fastapi import APIRouter, Depends, HTTPException, Response
from schemas.user_schema import UserCreate, User

router = APIRouter()

fake_users_db = [
    {"id": 1, "name": "Ana Torres", "email": "ana@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "messi ", "email": "messi@example.com", "role": "support", "is_active": True},
    {"id": 3, "name": "cristiano", "email": "cristiano@example.com", "role": "user", "is_active": False},
    {"id": 4, "name": "cristian", "email": "cristian@example.com", "role": "admin", "is_active": True},
]

@router.get("/users", response_model=list[User])
def listar_usuarios(response: Response, role: str = None, is_active: bool = None):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    resultado = fake_users_db
    if role is not None:
        resultado = [user for user in resultado if user["role"] == role]
    if is_active is not None:
        resultado = [user for user in resultado if user["is_active"] == is_active]
    return resultado


@router.get("/users/{user_id}", response_model=User)
def obtener_usuario(user_id: int, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/users", response_model=User)
def crear_usuario(user: UserCreate, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    if user.email in [u["email"] for u in fake_users_db]:
        raise HTTPException(status_code=409, detail="Correo electrónico ya registrado")

    new_user = user.model_dump()

    if fake_users_db:
        nuevo_id = max(u["id"] for u in fake_users_db) + 1
    else:
        nuevo_id = 1

    new_user["id"] = nuevo_id
    fake_users_db.append(new_user)
    return new_user