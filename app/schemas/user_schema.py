# # from enum import Enum
# # from pydantic import BaseModel, EmailStr, Field
# # from typing import Optional

# # class UserRole(str, Enum):
# #     admin = "admin"
# #     user = "user"
# #     support = "support"

# # class UserBase(BaseModel):
# #     email: EmailStr
# #     name: str = Field(min_length=3)
# #     role: UserRole
# #     is_active: bool

# # class UserCreate(UserBase):
# #     pass

# # class User(UserBase):
# #     id: int

# # class UserUpdate(BaseModel):
# #     email: Optional[EmailStr] = None
# #     name: Optional[str] = Field(default=None, min_length=3)
# #     role: Optional[UserRole] = None
# #     is_active: Optional[bool] = None

# 
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# 1. Definición correcta del Enum
class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    support = "support"

# Schema base
class Userbase(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: UserRole
    is_active: bool = True

# Schema para creación
class UserCreate(Userbase):
    pass

# 2. Schema para actualización completa (PUT)
class UserUpdate(Userbase):
    pass

# Schema para actualización parcial (PATCH)
class Userpatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# 3 y 4. Schema de respuesta completo para Pydantic v2
class UserResponse(Userbase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Reemplaza orm_mode = True