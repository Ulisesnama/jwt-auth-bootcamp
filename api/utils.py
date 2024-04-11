from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import User


def generate_jwt_token(user: User):
    payload = {
        "user_pk": user.pk,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
