from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Profile, Kool

def index(request):
    curr_date = datetime.now()
    context = {
        'auth_user' : request.user,
    }
    return render(request, 'koolack_unscaled/index.html', context)

def register(request):
    return HttpResponse('form to register! jk')

@login_required
def timeline(request):
    context = {
        'auth_user' : request.user,
        'kool_list' : Kool.objects.filter(author__profile__followed_by=request.user.profile).order_by('-creation_date'),
    }
    return render(request, 'koolack_unscaled/timeline.html', context)

def user(request, username):
    page_user = get_object_or_404(User, username=username)
    context = {
        'auth_user' : request.user,
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
