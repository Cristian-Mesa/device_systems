from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.auth.security import create_access_token
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.rate_limit import limiter
from app.schemas.auth_schema import Token, UserRegister
from app.schemas.user_schema import UserResponse


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit('3/minute')
def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = auth_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='El email ya esta registrado',
        )

    return auth_service.register_user(db, user_data)


@router.post('/login', response_model=Token)
@limiter.limit('5/minute')
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email o contrasena incorrectos',
        )

    access_token = create_access_token({'sub': user.email, 'role': user.role})
    return Token(access_token=access_token)


@router.get('/me', response_model=UserResponse, tags=['Security'])
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user