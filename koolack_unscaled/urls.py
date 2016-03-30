from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^timeline$', views.timeline, name='timeline'),
    url(r'^user/(?P<username>[a-z]+)/$', views.user, name='user'),
    url(r'^user/(?P<username>[a-z]+)/mentions/$', views.mentions, name='mentions'),
    url(r'^kool/(?P<kool_id>[0-9]+)$', views.kool, name='kool'),
    url(r'^tag/(?P<tag>[a-z]+)/$', views.tag, name='tag'),
]
