from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    support = "support"
    
class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=3)
    role: UserRole
    is_active: bool

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int