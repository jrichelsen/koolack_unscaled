from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin


from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile, Kool

class IndexView(TemplateView):
    template_name = 'koolack_unscaled/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['n_users'] = Profile.objects.count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/timeline')
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class TimelineView(SingleObjectMixin, ListView):
    paginate_by = 15
    template_name = 'koolack_unscaled/timeline.html'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super(TimelineView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Kool.objects.filter(author__profile__followed_by=self.object.profile)

class UserView(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = 'koolack_unscaled/user.html'
    slug_field = 'username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['page_user'] = self.object
        return context

    def get_queryset(self):
        return self.object.kool_set.all()

def mentions(request, username):
    return HttpResponse("mention page for %s" % username)

def follow(request, username):
    return HttpResponse("you are now following %s" % username)

def unfollow(request, username):
    return HttpResponse("you are not following %s" % username)

def kool(request, kool_id):
    return HttpResponse("kool %s" % kool_id)

def tag(request, tag):
    return HttpResponse("tag %s" % tag)
