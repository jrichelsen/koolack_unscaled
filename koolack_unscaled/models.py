from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False)

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


@python_2_unicode_compatible
class Kool(models.Model):
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.content
