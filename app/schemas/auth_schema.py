from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user_schema import UserRole


class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    role: UserRole = UserRole.user

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if " " in password:
            raise ValueError("La contrasena no puede tener espacios")
        if not any(character.isupper() for character in password):
            raise ValueError("La contrasena debe tener una mayuscula")
        if not any(character.islower() for character in password):
            raise ValueError("La contrasena debe tener una minuscula")
        if not any(character.isdigit() for character in password):
            raise ValueError("La contrasena debe tener un numero")
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    email: EmailStr | None = None

