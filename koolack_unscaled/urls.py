from django.conf.urls import url
import django.contrib.auth.views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

from . import views, forms

app_name = 'koolack_unscaled'
urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),
    url(r'^register$',
        CreateView.as_view(
            form_class=forms.RegisterForm,
            template_name='registration/register.html',
            success_url='/login'),
        name='register'),
    url(r'^login$',
        auth_views.login,
        name='login'),
    url(r'^logout$',
        auth_views.logout,
        {'next_page': '/'},
        name='logout'),
    url(r'^timeline$',
        login_required(views.TimelineView.as_view()),
        name='timeline'),
    url(r'^user/(?P<slug>\w+)/$',
        views.UserView.as_view(),
        name='user'),
    url(r'^user/(?P<username>[a-z]+)/mentions/$', views.mentions, name='mentions'),
    url(r'^user/(?P<username>[a-z]+)/follow$', views.follow, name='follow'),
    url(r'^user/(?P<username>[a-z]+)/unfollow$', views.unfollow, name='unfollow'),
    url(r'^kool/(?P<kool_id>[0-9]+)$', views.kool, name='kool'),
    url(r'^tag/(?P<tag>[a-z]+)/$', views.tag, name='tag'),
]
