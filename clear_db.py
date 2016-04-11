# needed to access Django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koolack_unscaled_proj.settings")
django.setup()

from django.contrib.auth.models import User

from koolack_unscaled.models import Profile

Profile.objects.all().delete()
User.objects.all().delete()
