"""
Main views class for the UX LABS API
"""
from collections import defaultdict
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.timezone import utc
from rest_framework import generics, permissions, status, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from formAPI import choices
from formAPI.models import FormAPI, Test, Appointment
from formAPI.pagination import CustomPaginationSerializer
from formAPI.serializers import \
    FormAPI_Serializer, \
    FormAPI_Serializer_Put, UserSerializer, \
    FormAPI_Serializer_Put_Validated, \
    TestSerializer, \
    AppointmentSerializer, UserSerializer_Superuser
import datetime
import django_filters
import json
import overload_exceptions

#Overloads
class overload_detail(object):
    """
    Overload for detail page
    """
    def put(self, request, pk, format=None):
        """
        Overloading put request
        """
        try:
            formAPI = FormAPI.objects.get(pk = pk)
            if request.user.is_authenticated():
                serializer = FormAPI_Serializer_Put_Validated(formAPI, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if not formAPI.completed_initial:
                serializer = FormAPI_Serializer_Put(formAPI, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            error_return = {"detail": str(error)}
            return Response(error_return, \
                status=status.HTTP_400_BAD_REQUEST)

class overload_list(object):
    """
    Class used to overload in api list
    """
    def post(self, request, *args, **kwargs):
        """
        Overloading post request
        """
        count_query = FormAPI.objects.filter(email=request.DATA['email'])
        count_used = count_query.count()
        if count_used > 0:
            response = {
                'error': 'email',
                'detail': 'Email has already been registered'
            }
            return HttpResponse(json.dumps(response),
                status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        """
        Return list of participants
        """
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
    Permission for the list
    Allowed if authenticated or 'POST'
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
    Permission will be granted to:
    Authenticated users,
    Requests originating from a 'PUT'
    """
    def has_permission(self, request, view):
        """
        Checks to see whether or not to give permission
        If user is authenticated or posting it should give permission
        Else it should return false
        """
        if request.user.is_authenticated():
            return True
        elif request.method == 'PUT':
            try:
                r_participant = FormAPI.objects.get(pk=view.kwargs['pk'])
            except Exception, e:
                return False
            if not r_participant.completed_initial:
                return True
        else:
            return False

class user_permissions(permissions.BasePermission):
    """
    Permission will be granted only to authenticated users
    """
    def has_permission(self, request, view):
        """
        Checks to see whether or not to give permission
        only allow if auth
        """
        if request.user.is_authenticated() and request.method == 'DELETE':
            return True
        if request.user.is_authenticated():
            return True
        return False


#Views
class FormAPIList(overload_list, generics.ListCreateAPIView):
    """
    Class for listing out all participants
    """
    pagination_serializer_class = CustomPaginationSerializer
    permission_classes = (list_permissions, )
    queryset = FormAPI.objects.all()
    serializer_class = FormAPI_Serializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, )
    ordering = ('-completed_initial', '-created')
    ordering_fields = 'name', 'email', 'created', 'id', 'state', \
        'completed_initial'
    def get_queryset(self):
        search_dict = dict(self.request.QUERY_PARAMS.lists())
        queryset = FormAPI.objects.all()
        if 'state' in search_dict:
            queryset = queryset.filter\
                (state__in=[str(x) for x in search_dict['state']])
        if 'completed_initial' in search_dict:
            queryset = queryset.filter\
                (completed_initial__in=\
                    [str(x) for x in search_dict['completed_initial']])
        if 'job' in search_dict:
            queryset = queryset.filter\
                (job__in=[str(x) for x in search_dict['job']])
        if 'employment' in search_dict:
            queryset = queryset.filter\
                (employment__in=[str(x) for x in search_dict['employment']])
        if 'income' in search_dict:
            queryset = queryset.filter\
                (income__in=[str(x) for x in search_dict['income']])
        if 'experience' in search_dict:
            queryset = queryset.filter\
                (experience__in=[str(x) for x in search_dict['experience']])
        if 'hoursOnline' in search_dict:
            queryset = queryset.filter\
                (hoursOnline__in=[str(x) for x in search_dict['hoursOnline']])
        if 'educationLevel' in search_dict:
            queryset = queryset.filter\
                (educationLevel__in=\
                    [str(x) for x in search_dict['educationLevel']])
        if 'participateTime' in search_dict:
            queryset = queryset.filter\
                (participateTime__in=\
                    [str(x) for x in search_dict['participateTime']])
        if 'gender' in search_dict:
            queryset = queryset.filter\
            (gender__in=[str(x) for x in search_dict['gender']])
        return queryset


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
    paginate_by = None
    permission_classes = (user_permissions, )
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserSerializer_Superuser
        else:
            return UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed user view
    """
    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserSerializer_Superuser
        else:
            return UserSerializer
    permission_classes = (user_permissions, )
    queryset = User.objects.all()


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
            token.created < utc_now - datetime.timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), \
                content_type="application/json")
        raise overload_exceptions.IncorrectLogin()
obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()


class ObtainChoices(choices_overload, generics.RetrieveAPIView):
    """
    Obtains choices from backend
    """
    permission_classes = (permissions.AllowAny,)
obtain_choices = ObtainChoices.as_view()


class Logout(generics.CreateAPIView):
    """
    Logout endpoint
    Uses post to send logout and delete token from backend
    """
    def post(self, request):
        """
        Catches post request from the front end
        """
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
logout = Logout.as_view()

class CheckValidSignUp(generics.CreateAPIView):
    """
    Checks if user should be able to sign up or not
    Returns id, name, email if allowed
    Else it returns a 400 - Bad Request
    """
    def post(self, request):
        """
        Catches post request from the front end
        """
        try:
            encoded_data = request.DATA['hashed']
            participant_to_check =  FormAPI.objects.get(hashInit = encoded_data)
            assert participant_to_check.completed_initial == False
            response_data = {}
            response_data['id'] = participant_to_check.id
            response_data['name'] = participant_to_check.name
            response_data['email'] = participant_to_check.email
            return HttpResponse(json.dumps(response_data), \
                content_type="application/json")
        except Exception:
            response_data = {}
            response_data['detail'] = "Already filled out"
            return HttpResponse(json.dumps(response_data), \
                status=status.HTTP_400_BAD_REQUEST)
check_valid_sign_up = CheckValidSignUp.as_view()


class TestList(generics.ListCreateAPIView):
    """
    Class for listing out all tests
    """
    paginate_by = None
    permission_classes = (user_permissions, )
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for detail test view
    """
    permission_classes = (user_permissions, )
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class AppointmentList(generics.ListCreateAPIView):
    """
    Class for listing out all appointments
    """
    paginate_by = None
    permission_classes = (user_permissions, )
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for detail appointment view
    """
    permission_classes = (user_permissions, )
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    Class for change password link
    """
    def put(self, request):
        user = request.user
        try:
            print user
            print type(user)
            print user.check_password(request.DATA['oldPassword'])
            if user.check_password(request.DATA['oldPassword']):
                user.set_password(request.DATA['newPassword'])
                user.save()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        except Exception, e:
            response_data = {}
            response_data['detail'] = e
            return HttpResponse(json.dumps(response_data), \
                status=status.HTTP_400_BAD_REQUEST)
