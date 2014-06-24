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

class overload(object):
    def post(self, request, *args, **kwargs ):
        try:
            validate_email((request.DATA).__getitem__('email')) #[]
        except Exception as error:
            return self.create(request, *args, **kwargs)
        # email = EmailMessage(
        #     "Link to complete application", 
        #     "Please go to $LINK\nto complete your application", 
        #     to=[(request.DATA).__getitem__('email')]
        # )
        # email.send()
        response = self.create(request, *args, **kwargs)
        return response
class FormAPIList(overload, generics.ListCreateAPIView):
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer

class overload2(object):
    def put(self, request, pk, format=None):
        formAPI = FormAPI.objects.get(pk = pk)
        print formAPI.__getitem__()
        serializer = FormAPI_Serializer_Put(formAPI, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class FormAPIDetail(overload2, generics.RetrieveUpdateDestroyAPIView):
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer