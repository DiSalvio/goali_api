from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

def token_expires_in(token):
    time_elapsed = timezone.now() - token.created
    return timedelta(seconds=float(settings.TOKEN_EXPIRED_AFTER_SECONDS)) - time_elapsed


def is_token_expired(token):
    return token_expires_in(token) < timedelta(seconds=0)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if is_token_expired(token):
            token.delete()
            raise AuthenticationFailed("The Token is expired")
        
        return (token.user, token)
