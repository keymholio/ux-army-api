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
)

urlpatterns = format_suffix_patterns(urlpatterns)