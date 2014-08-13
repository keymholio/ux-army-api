from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from formAPI import views

urlpatterns = patterns('',
    url(r'^$', 'api_root'),
    url(r'^api/$',
        views.FormAPIList.as_view(),
        name='formAPI-list'),
    url(r'^api/(?P<pk>[0-9]+)/$',
        views.FormAPIDetail.as_view(),
        name='formAPI-detail'),
    url(r'^users/$', 
   		views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', 
		views.UserDetail.as_view()),
    url(r'^login/', 'formAPI.views.obtain_expiring_auth_token'),
    url(r'^choices/', 'formAPI.views.obtain_choices'),
    url(r'^logout/', 'formAPI.views.logout'),
    url(r'^demo-form-check/', 'formAPI.views.check_valid_sign_up'),
    url(r'^tests/$',
        views.TestList.as_view(),
        name='test-list'),
    url(r'^tests/(?P<pk>[0-9]+)/$',
        views.TestDetail.as_view(),
        name='test-detail'),
    url(r'^appointments/$',
        views.AppointmentList.as_view(),
        name='appointment-list'),
    url(r'^appointments/(?P<pk>[0-9]+)/$',
        views.AppointmentDetail.as_view(),
        name='appointment-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
