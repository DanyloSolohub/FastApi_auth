import re
from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException


class LoginSerializer(BaseModel):
    username: EmailStr
    password: str

    @validator('password')
    def passwords_match(cls, password, **kwargs):
        regex = r'((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,40})\S$'
        result = re.findall(regex, password)
        if not result:
            raise HTTPException(status_code=400,
                                detail='password must be minimum of 6 characters, at least 1 uppercase letter,'
                                       '1 lowercase letter, and 1 num with no spaces.')
        return password

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
