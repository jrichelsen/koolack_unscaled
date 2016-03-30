from django.http import HttpResponse

from .models import Profile, Kool

def index(request):
    return HttpResponse('blurb about site, links to register and login')

def timeline(request):
    return HttpResponse('this is timeline')

def user(request, username):
    return HttpResponse("user page for %s" % username)

def mentions(request, username):
    return HttpResponse("mention page for %s" % username)

def kool(request, kool_id):
    return HttpResponse("kool %s" % kool_id)

def tag(request, tag):
    return HttpResponse("tag %s" % tag)
