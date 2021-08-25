from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from fastapi_mail import FastMail, MessageSchema

from utils.database import ACCESS_TOKEN_EXPIRE_MINUTES, Session
from users.models.user import User
from users.auth_.serializers import LoginSerializer
from users.serializers import UserSerializer
from utils.exceptions import incorrect_password, user_already_exist
from utils.email_sending import conf
from users.auth_.services import (pwd_context, get_user_or_404, get_current_active_user,
                                  create_access_token, create_user, get_current_user)

auth_router = APIRouter(prefix='/api/v1')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


@auth_router.post('/authorization', status_code=status.HTTP_201_CREATED)
async def authorization(form_data: LoginSerializer):
    user_instance = Session.query(User).filter(User.email == form_data.username).first()
    if user_instance:
        raise user_already_exist
    user = create_user(form_data)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    message_to_send = f'Activate account - http://127.0.0.1:8000/api/v1/activate?token={access_token}'
    message = MessageSchema(
        subject="Активация аккаунта",
        recipients=[user.email],
        body=message_to_send,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {'status': 'success'}


@auth_router.get('/activate', response_model=UserSerializer)
async def activate_by_email(token: str):
    user = get_current_user(token=token)
    if not user.is_active:
        user.is_active = True
        user.save()
    return user


@auth_router.post('/token')
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_instance = get_user_or_404(form_data.username)
    if not pwd_context.verify(form_data.password, user_instance.password):
        raise incorrect_password
    access_token = create_access_token(
        data={"sub": user_instance.email}, expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/current_user/", response_model=UserSerializer)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
