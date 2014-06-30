from rest_framework import generics, mixins, permissions, renderers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from formAPI.models import FormAPI
from formAPI.serializers import FormAPI_Serializer, FormAPI_Serializer_Put

class MyUserPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print request.method
        if request.method == 'POST':
            return True
        if request.method == 'GET':
            if request.user.is_authenticated():
                return True
            return False
        if request.method in permissions.SAFE_METHODS:
            return False
        # Instance must have an attribute named `owner`

class overload_post(object):
    permission_classes = (MyUserPermissions, )
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
    #print request.method
    permission_classes = (MyUserPermissions, )
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