from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from datetime import datetime

from .models import Profile, Kool

def index(request):
    curr_date = datetime.now()
    context = {
        'curr_date' : curr_date,
    }
    return render(request, 'koolack_unscaled/index.html', context)

def login(request):
    return HttpResponse('jk, cannot login yet')

def logout(request):
    return HttpResponse('cannot logout either')

def register(request):
    return HttpResponse('form to register! jk')

def timeline(request):
    return HttpResponse('this is timeline')

def user(request, username):
    prof = get_object_or_404(Profile, user__username=username)
    context = {
        'prof' : prof,
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
