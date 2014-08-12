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
    url(r'^tasks/$',
        views.TaskList.as_view(),
        name='task-list'),
    url(r'^tasks/(?P<pk>[0-9]+)/$',
        views.TaskDetail.as_view(),
        name='task-detail'),
    url(r'^events/$',
        views.EventList.as_view(),
        name='event-list'),
    url(r'^events/(?P<pk>[0-9]+)/$',
        views.EventDetail.as_view(),
        name='event-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
