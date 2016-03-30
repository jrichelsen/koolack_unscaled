from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def __str__(self):
        return self.user.username

@python_2_unicode_compatible
class Kool(models.Model):
    contents = models.CharField(max_length=140)
    author = models.ForeignKey(Profile)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contents
