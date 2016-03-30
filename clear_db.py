# needed to access Django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koolack_unscaled_proj.settings")
django.setup()

from django.contrib.auth.models import User
from django.db.models import Q

from koolack_unscaled.models import Profile

# delete all Profiles (will delete all Users linked to a Profile)
Profile.objects.all().delete()

# delete all straggler Users EXCEPT admin
# necessary because there may exist Users not associated with a Profile
User.objects.filter(~Q(username='admin')).delete()
