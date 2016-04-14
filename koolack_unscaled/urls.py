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
    url(r'^user/(?P<username>\w+)/$',
        views.UserView.as_view(),
        name='user'),
    url(r'^user/(?P<username>\w+)/follow$',
        login_required(views.FollowView.as_view()),
        name='follow'),
    url(r'^user/(?P<username>\w+)/unfollow$',
        login_required(views.UnfollowView.as_view()),
        name='unfollow'),
    url(r'^kool/(?P<pk>\d+)/ack$',
        views.AckView.as_view(),
        name='ack'),
    url(r'^kool/(?P<pk>\d+)/unack$',
        login_required(views.UnackView.as_view()),
        name='unack'),
    url(r'^ref/(?P<ref>[^\s]+)/$',
        views.RefView.as_view(),
        name='ref'),
    url(r'^about$',
        views.about,
        name='about'),
    url(r'^privacy$',
        views.privacy,
        name='privacy'),
]
