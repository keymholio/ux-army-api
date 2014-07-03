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
      url(r'^api-token-auth/', 'formAPI.views.obtain_expiring_auth_token')
)

urlpatterns = format_suffix_patterns(urlpatterns)