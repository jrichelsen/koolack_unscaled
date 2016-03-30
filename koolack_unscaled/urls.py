from django.conf.urls import url

from . import views

app_name = 'koolack_unscaled'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^timeline$', views.timeline, name='timeline'),
    url(r'^user/(?P<username>[a-z]+)/$', views.user, name='user'),
    url(r'^user/(?P<username>[a-z]+)/mentions/$', views.mentions, name='mentions'),
    url(r'^user/(?P<username>[a-z]+)/follow$', views.follow, name='follow'),
    url(r'^user/(?P<username>[a-z]+)/unfollow$', views.unfollow, name='unfollow'),
    url(r'^kool/(?P<kool_id>[0-9]+)$', views.kool, name='kool'),
    url(r'^tag/(?P<tag>[a-z]+)/$', views.tag, name='tag'),
]
