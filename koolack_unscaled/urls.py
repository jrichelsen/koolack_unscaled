from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
import django.contrib.auth.views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls import patterns

from . import views, forms

app_name = 'koolack_unscaled'
urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),
    url(r'^register$',
        CreateView.as_view(
            template_name='registration/register.html',
            form_class=forms.RegisterForm,
            success_url=reverse_lazy('koolack_unscaled:timeline')),
        name='register'),
    url(r'^login$',
        auth_views.login,
        name='login'),
    url(r'^logout$',
        auth_views.logout,
        {'next_page': reverse_lazy('koolack_unscaled:index')},
        name='logout'),
    url(r'^timeline$',
        login_required(views.TimelineView.as_view()),
        name='timeline'),
    url(r'^user/(?P<username>[^\s]+)/$',
        views.UserView.as_view(),
        name='user'),
    url(r'^user/(?P<username>[^\s]+)/follow$',
        login_required(views.FollowView.as_view()),
        name='follow'),
    url(r'^user/(?P<username>[^\s]+)/unfollow$',
        login_required(views.FollowView.as_view(unfollow=True)),
        name='unfollow'),
    url(r'^kool/(?P<pk>\d+)/ack$',
        views.AckView.as_view(),
        name='ack'),
    url(r'^hashtag/(?P<tag>[^\s]+)/$',
        views.HashtagView.as_view(),
        name='hashtag'),
    url(r'^about$',
        views.AboutView.as_view(),
        name='about'),
]

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}))
