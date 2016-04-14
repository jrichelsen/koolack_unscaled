from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

@python_2_unicode_compatible
class Ref(models.Model):
    tag = models.CharField(max_length=139)

    def __str__(self):
        return self.tag

@python_2_unicode_compatible
class Kool(models.Model):
    content = models.CharField(max_length=140)
    refs = models.ManyToManyField(
        Ref,
        related_name='reffed_in',
        symmetrical=False)
    href_content = models.TextField(editable=False)
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):        
        tags = set(part[1:] for part in self.content.split() if part.startswith('$'))
        href_tokens = list()
        for token in self.content.split():
            if token[1:] in tags:
                token = '<a href="' + reverse('koolack_unscaled:ref', args=[token[1:]]) + '">' + token + '</a>'
            href_tokens.append(token)
        self.href_content = ' '.join(href_tokens)
        super(Kool, self).save(*args, **kwargs)
        for tag in tags:
            self.refs.add(Ref.objects.get_or_create(tag=tag)[0])

@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False)
    acks = models.ManyToManyField(
        Kool,
        related_name='acked_by',
        symmetrical=True)

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
