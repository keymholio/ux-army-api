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

class FormAPIList(overload_post, generics.ListCreateAPIView):
    """
    Class for listing out all participants
    """
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
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer