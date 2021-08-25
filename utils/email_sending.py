from fastapi_mail import ConnectionConfig
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_USERNAME'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Confirm your email address",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)
