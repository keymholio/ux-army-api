from rest_framework import generics, mixins, permissions, renderers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from formAPI.models import FormAPI
from formAPI.serializers import FormAPI_Serializer, FormAPI_Serializer_Put, UserSerializer



import datetime
from django.utils.timezone import utc
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.timezone import utc
from rest_framework import exceptions


class list_permissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        """
        Checks to see whether or not to give permission
        If user is authenticated or posting it should give permission
        Else it should return false
        """
        print request.method
        if request.user.is_authenticated():
                return True
        if request.method == 'POST':
            return True
        return False

class overload_post(object):
    def post(self, request, *args, **kwargs ):
        """
        Overloading post request
        """
        try:
            validate_email((request.DATA).__getitem__('email'))
        except Exception as error:
            return self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class FormAPIList(overload_post, generics.ListCreateAPIView):
    """
    Class for listing out all participants
    """
    permission_classes = (list_permissions, )
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer


class overload_put(object):

    def put(self, request, pk, format=None):
        """
        Overloading put request
        """
        formAPI = FormAPI.objects.get(pk = pk)
        serializer = FormAPI_Serializer_Put(formAPI, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormAPIDetail(overload_put, generics.RetrieveUpdateDestroyAPIView):
    """
    Class for detail participant view
    """
    # permission_classes = (MyUserPermissions, )
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer


class UserList(generics.ListCreateAPIView):#generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request):
#         serializer = self.serializer_class(data=request.DATA)
#         if serializer.is_valid():
#             token, created =  Token.objects.get_or_create(user=serializer.object['user'])

#             if not created:
#                 # update the created time of the token to keep it valid
#                 token.created = datetime.datetime.utcnow()
#                 token.save()

#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer_class = AuthTokenSerializer
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])
            utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
            if not created and token.created < utc_now - datetime.timedelta(minutes=1):
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        # raise exceptions.AuthenticationFailed('Invalid username/password')
        #response_data = {'detail': 'Invalid username/password'}
        return HttpResponse(json.dumps(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        #return HttpResponse(json.dumps(response_data), status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()