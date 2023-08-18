import os

import jwt
from django.contrib.auth import login
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from referral_app.api.models import User

from .exceptions import (
    InvalidAuthorizationCode,
    PhoneDoesNotExist,
    TokenAuthorizationExpiredError,
    TokenAuthorizationInvalidError,
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_token = auth_header.decode("utf-8")

        if not auth_token:
            raise TokenAuthorizationInvalidError()

        try:
            decoded_data = jwt.decode(
                jwt=auth_token, key=SECRET_KEY, algorithms=["HS256"]
            )
            phone_number = decoded_data.get("phone_number")

            user = User.objects.get(phone_number=phone_number)

            return user, auth_token

        except jwt.DecodeError:
            raise TokenAuthorizationExpiredError()
        except jwt.ExpiredSignature:
            raise TokenAuthorizationInvalidError()
        except User.DoesNotExist:
            raise PhoneDoesNotExist()

        return super().authenticate(request)


def authenticate_user(request) -> [User | None]:
    phone_number = request.data.get("phone_number", None)
    authorization_code = request.data.get("authorization_code", None)

    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        raise PhoneDoesNotExist()

    if user.authorization_code != authorization_code:
        raise InvalidAuthorizationCode()

    login(request, user)
    return user
