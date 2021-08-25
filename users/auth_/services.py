from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from utils.exceptions import credentials_exception, inactive_user, user_not_found
from utils.database import SECRET_KEY, ALGORITHM
from users.models.user import User
from users.auth_.serializers import TokenData, LoginSerializer
from utils.database import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_or_404(username: str) -> User:
    user_instance: User = Session.query(User).filter(User.email == username).first()
    if not user_instance:
        raise user_not_found
    return user_instance


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
    username: str = payload.get("sub")
    if not username:
        raise credentials_exception
    token_data = TokenData(email=username)
    user = get_user_or_404(username=token_data.email)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise inactive_user
    return current_user


def create_user(user: LoginSerializer) -> User:
    user = User.create(email=user.username, password=pwd_context.hash(user.password))
    return user
