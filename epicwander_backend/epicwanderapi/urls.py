from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from django.views.decorators.csrf import csrf_exempt

from epicwanderapi import views



urlpatterns = patterns('',
    
	url(r'^api/users/$', views.UserList.as_view()),
	url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	#url(r'^api/user_photos', csrf_exempt(views.PhotoViewSet)),
	#url(r'^api/user_photos_mpp', views.PhotoMultiPartParserViewSet),
)

urlpatterns = format_suffix_patterns(urlpatterns)