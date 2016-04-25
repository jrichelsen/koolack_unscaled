from django.views.generic import TemplateView, View, ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profile, Kool, Hashtag
from .forms import KoolForm

KOOLS_PER_PAGE = 15

class IndexView(TemplateView):
    template_name = 'koolack_unscaled/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['n_users'] = Profile.objects.count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('koolack_unscaled:timeline'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class TimelineView(MultipleObjectMixin, CreateView):
    template_name = 'koolack_unscaled/timeline.html'
    model = Kool
    form_class = KoolForm
    paginate_by = KOOLS_PER_PAGE
    success_url = reverse_lazy('koolack_unscaled:timeline')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(TimelineView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Kool.objects.filter(author__profile__followed_by=self.request.user.profile)

    def form_valid(self, form):
        print form.fields['image'].required
        form.instance.author = self.request.user
        return super(TimelineView, self).form_valid(form)

class UserView(SingleObjectMixin, ListView):
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'koolack_unscaled/user.html'
    paginate_by = 15

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['page_user'] = self.object
        if self.request.user == self.object:
            context['form'] = KoolForm()
        else:
            if self.request.user.is_authenticated():
                context['unfollow_button'] = self.request.user.profile.follows.filter(user=self.object).exists()
                context['follow_button'] = not context['unfollow_button']
            else:
                context['follow_button'] = True
        return context

    def get_queryset(self):
        return self.object.kool_set.all()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        form = KoolForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            kool = form.save(commit=False)
            kool.author = request.user
            kool.save()
            return HttpResponseRedirect(reverse('koolack_unscaled:user', kwargs={'username': self.object.username}))
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, 'koolack_unscaled/user.html', context)            

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

class HashtagView(SingleObjectMixin, ListView):
    slug_url_kwarg = 'tag'
    slug_field = 'tag'
    template_name = 'koolack_unscaled/hashtag.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Hashtag.objects.all())
        return super(HashtagView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HashtagView, self).get_context_data(**kwargs)
        context['hashtag'] = self.object
        return context

    def get_queryset(self):
        return self.object.hashtagged_in.all()

class AboutView(TemplateView):
    template_name = 'koolack_unscaled/about.html'

class PrivacyView(TemplateView):
    template_name = 'koolack_unscaled/privacy.html'
