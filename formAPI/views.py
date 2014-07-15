"""
Main views class for the UX LABS API
"""
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from formAPI import choices
from formAPI.models import FormAPI
from formAPI.serializers import FormAPI_Serializer, FormAPI_Serializer_Put, UserSerializer
import datetime
import json

#Overloads
class overload_detail(object):
    """
    Overload for detail page
    """
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

class overload_list(object):
    """
    Class used to overload in api list
    """
    def post(self, request, *args, **kwargs):
        """
        Overloading post request
        """
        return self.create(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class choices_overload(object):
    """
    Class used to overload choice calls
    """
    def get(self, request, *args, **kwargs):
        """
        Overloading put request
        """
        response_data = choices.get_choices()
        return HttpResponse(json.dumps(response_data), content_type="application/json")


#Permissions
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
        if request.user.is_authenticated():
            return True
        if request.method == 'POST':
            return True
        return False

class detail_permissions(permissions.BasePermission):
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
        if request.user.is_authenticated():
            return True
        if request.method == 'PUT':
            return True
        return False

class user_permissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        """
        Checks to see whether or not to give permission
        only allow if auth
        """
        if request.user.is_authenticated():
            return True
        return False

class choice_permissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        """
        Checks to see whether or not to give permission
        """
        if request.user.is_authenticated():
            print 'IS'
        if not request.user.is_authenticated():
            print 'IS NOT'
        if request.method == 'GET':
            return True
        return False


#Views
class FormAPIList(overload_list, generics.ListCreateAPIView):
    """
    Class for listing out all participants
    """
    permission_classes = (list_permissions, )
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer


class FormAPIDetail(overload_detail, generics.RetrieveUpdateDestroyAPIView):
    """
    Class for detail participant view
    """
    permission_classes = (detail_permissions, )
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer


class UserList(generics.ListCreateAPIView):
    """
    User list view
    """
    #permission_classes = (user_permissions, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Detailed user view
    """
    #permission_classes = (user_permissions, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ObtainExpiringAuthToken(ObtainAuthToken):
    """
    Class to obtain auth token
    Token should expire after a given amount of time
    """
    def post(self, request):
        """
        Catches post request from the front end
        """
        serializer_class = AuthTokenSerializer
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  \
                Token.objects.get_or_create(user=serializer.object['user'])
            utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
            if not created and \
            token.created < utc_now - datetime.timedelta(minutes=5):
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), \
                content_type="application/json")
        return HttpResponse(json.dumps(serializer.errors), \
            status=status.HTTP_400_BAD_REQUEST)
obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()


class ObtainChoices(choices_overload, generics.RetrieveAPIView):
    """
    Obtains choices from backend
    Does not allow anything other than GET
    """
    #permission_classes = (choice_permissions, )
    permission_classes = (permissions.AllowAny,)
obtain_choices = ObtainChoices.as_view()

#Leaving this here for future use
# class Logout(generics.CreateAPIView):
#     """
#     Logout
#     """
#     def post(self, request):
#         """
#         Catches post request from the front end
#         """
#         response_data = {}
#         return HttpResponse(json.dumps(response_data), \
#         content_type="application/json")
# logout = Logout.as_view()

@csrf_exempt
def logout(request):
    """
    Used to logout
    CSRF is exempt (only internal)
    """
    if request.method == 'POST':
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header is not None:
            tokens = auth_header.split(' ')
            if len(tokens) == 2 and tokens[0] == 'Token':
                token = tokens[1]
                user = User.objects.filter(auth_token=token)
                if user .count() != 0:
                    token = Token.objects.get_or_create(user=user)[0]
                    token.delete()
        response_data = {}
        return HttpResponse(json.dumps(response_data), \
        content_type="application/json")
