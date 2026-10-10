from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nombre: str
    correo: EmailStr
    id_rol: int

class UserCreate(UserBase):
    contrasena: str

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    contrasena: Optional[str] = None

class UserResponse(UserBase):
    id_usuario: int

    class Config:
        from_attributes = True