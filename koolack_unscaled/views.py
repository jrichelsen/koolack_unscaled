from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

def register(request):
    return HttpResponse('form to register! jk')

@login_required
def timeline(request):
    context = {
        'kool_list' : Kool.objects.filter(author__profile__followed_by=request.user.profile).order_by('-creation_date'),
    }
    return render(request, 'koolack_unscaled/timeline.html', context)

def user(request, username):
    page_user = get_object_or_404(User, username=username)
    context = {
        'page_user' : page_user,
        'kool_list' : page_user.kool_set.all().order_by('-creation_date'),
    }
    return render(request, 'koolack_unscaled/user.html', context)

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
