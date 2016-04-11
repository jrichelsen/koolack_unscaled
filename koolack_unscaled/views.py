from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse

from .models import Profile, Kool
from .forms import KoolForm

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
    template_name = 'koolack_unscaled/timeline.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super(TimelineView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Kool.objects.filter(author__profile__followed_by=self.object.profile)

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['form'] = KoolForm()
        return context

    def post(self, request, *args, **kwargs):
        kool_form = KoolForm(data=request.POST)
        if kool_form.is_valid():
            kool = kool_form.save(commit=False)
            kool.author = request.user
            kool.save()
        return HttpResponseRedirect('/timeline')

class UserView(SingleObjectMixin, ListView):
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'koolack_unscaled/user.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['page_user'] = self.object
        if self.request.user != self.object:
            context['unfollow_button'] = self.request.user.profile.follows.filter(user=self.object).exists()
            context['follow_button'] = not context['unfollow_button']
        return context

    def get_queryset(self):
        return self.object.kool_set.all()

class FollowView(SingleObjectMixin, View):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.follows.add(self.object.profile)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UnfollowView(SingleObjectMixin, View):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.follows.remove(self.object.profile)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AckView(SingleObjectMixin, View):
    model = Kool

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {
            'acker_list' : self.object.acked_by.all(),
        }
        return render(request,
            'koolack_unscaled/ack.html',
            context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.acks.add(self.object)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UnackView(SingleObjectMixin, View):
    model = Kool

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.acks.remove(self.object)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def kool(request, kool_id):
    return HttpResponse("kool %s" % kool_id)

def tag(request, tag):
    return HttpResponse("tag %s" % tag)
