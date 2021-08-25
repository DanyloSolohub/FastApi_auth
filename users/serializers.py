from pydantic import BaseModel, EmailStr


class UserSerializer(BaseModel):
    email: EmailStr
    name: str = None
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserDetailSerializer(BaseModel):
    email: EmailStr
    name: str = None
    is_active: bool
    is_superuser: bool
    name_ukr: str = None
    name_eng: str = None

    class Config:
        orm_mode = True
