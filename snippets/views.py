from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, SnippetSerializer_other
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
# from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import mixins
from rest_framework import generics
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework import status


class overload(object):
    def post(self, request, *args, **kwargs ):
        email = EmailMessage("Link to complete application", "Please go to ($link here)\nto complete your application", to=['APPLICANT@email.com'])
        email.send()
        # print(Snippet.objects.get(name = "Sarah", phone = '5555550000').name)
        print(request)
        print self
        return self.create(request, *args, **kwargs)


class SnippetList(overload, generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # Snippet.objects.filter(name = "Sarahh").update(phone = '5555550000')
    # print(Snippet.objects.get(name = "Sarah", phone = '5555550000').name)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # def pre_save(self, obj):
    #     obj.owner = self.request.user
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         print("POSTING")
#         return self.create(request, *args, **kwargs)


class overload2(object):
    # def get_object(self, pk):
    #     try:
    #         return Snippet.objects.get(pk=pk)
    #     except Snippet.DoesNotExist:
    #         raise Http404

    def put(self, request, pk, format=None):
        print (request.DATA).__getitem__('name')
        snippet = Snippet.objects.get(name = (request.DATA).__getitem__('name'))
        serializer = SnippetSerializer_other(snippet, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SnippetDetail(overload2, generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      # IsOwnerOrReadOnly,)
    # def pre_save(self, obj):
    #     obj.owner = self.request.user
    
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
    
# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })
