from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.auth.security import decode_access_token
from app.dependencies.database_dependency import get_db
from app.models.user_model import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception

    email = token_data.get("sub")
    if email is None:
        raise credentials_exception

    user = auth_service.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario esta inactivo",
        )

    return current_user

def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere el rol admin",
        )

    return current_user


def require_admin_or_support(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere el rol admin o support",
        )

    return current_user