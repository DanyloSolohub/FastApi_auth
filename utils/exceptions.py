from fastapi import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
user_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
incorrect_password = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='password incorrect')
user_already_exist = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail='User with this email already register')
