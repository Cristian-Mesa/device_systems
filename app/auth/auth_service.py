from sqlalchemy.orm import Session

from app.auth.security import get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def register_user(db: Session, user_data: UserRegister) -> User:
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role.value,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)

    if user is None or not user.hashed_password:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
