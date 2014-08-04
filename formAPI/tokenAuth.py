"""
Used to overload built in Token Authentication
Token will be valid for a specific time
"""
from django.utils.timezone import utc
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
import datetime

class ExpiringTokenAuth(TokenAuthentication):
    """
    Builds upon Django REST's original Token Authentication class
    """
    def authenticate_credentials(self, key):
        """
        Used to check if the token is valid or not
        """
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if token.created < utc_now - datetime.timedelta(hours=24):
            raise exceptions.AuthenticationFailed('Token has expired')
        return (token.user, token)
