import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koolack_unscaled_proj.settings")
django.setup()

import sys
from os import listdir
from os.path import isfile, join
import random

from django.contrib.auth.models import User
from django.core.files import File

from koolack_unscaled.models import Profile, Kool

N_KOOL_MIN = 10
N_KOOL_MAX = 200
IMAGE_DIRN = 'test_images'
N_FOLLOW_MIN = 1
N_FOLLOW_MAX = 100

n_users = int(sys.argv[1])

images = [File(open(join(IMAGE_DIRN, f))) for f in listdir(IMAGE_DIRN) if isfile(join(IMAGE_DIRN, f))]

# create Profiles (and the Users they contain) and their Kools
for user_n in xrange(n_users):
    my_username = 'testuser' + str(user_n)
    print 'creating ' + my_username

    my_user = User(
        username=my_username,
        first_name='Test',
        last_name='User'+str(user_n))
    my_user.set_password('koolack_unscaled')
    my_user.save()

    my_prof = Profile(user=my_user)
    my_prof.save()

    for kool_n in xrange(random.randint(N_KOOL_MIN, N_KOOL_MAX)):
        my_user.kool_set.create(
            content='this is #test #kool #'+str(kool_n)+' for me',
            image=random.choice(images))

# make Profiles follow one another (all Profiles must be created first)
print 'creating follow connections'
for user_n in xrange(n_users):
    my_prof = Profile.objects.get(user__username='testuser'+str(user_n))

    for user_n_to_follow in random.sample(xrange(n_users), random.randint(N_FOLLOW_MIN, N_FOLLOW_MAX)):
        my_prof.follows.add(Profile.objects.get(user__username='testuser'+str(user_n_to_follow)))
