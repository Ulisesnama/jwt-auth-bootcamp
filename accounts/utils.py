from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import User


def generate_jwt_tokens(user: User):
    access_payload = {
        "user_pk": user.pk,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    access_token = jwt.encode(
        access_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    refresh_payload = {
        "user_pk": user.pk,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    refresh_token = jwt.encode(
        refresh_payload, f"refresh.{settings.SECRET_KEY}", algorithm="HS256"
    )

    return access_token, refresh_token
