# needed to access Django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koolack_unscaled_proj.settings")
django.setup()

from django.contrib.auth.models import User
from collections import namedtuple

from koolack_unscaled.models import Profile, Kool

DummyUser = namedtuple('DummyUser', ['username', 'first_name', 'last_name', 'kool_contentses', 'follows_usernames'])

philos = [
    DummyUser(
        'cogitus',
        'Rene',
        'Descarte',
        [
            'I think, I am.',
        ],
        [
            'actuspurus',
        ]
    ),
    DummyUser(
        'one',
        'Benedict',
        'Spinoza',
        [
            'All is one, bruh',
        ],
        [
            'cogitus',
            'actuspurus',
            'hungrymonad',
        ]
    ),
    DummyUser(
        'constantconjunction',
        'David',
        'Hume',
        [
            'messed with billiards player everywhere, necesarrily',
        ],
        [
            'cogitus',
            'actuspurus',
            'hungrymonad',
        ]
    ),
    DummyUser(
        'actuspurus',
        'Thomas',
        'Aquinas',
        [
            'no happiness after life',
        ],
        []
    ),
    DummyUser(
        'hungrymonad',
        'Gottfried',
        'Leibniz',
        [
            "I'm so strange rn",
        ],
        [
            'cogitus', 
            'one',
            'actuspurus',
            'luckylocke',
        ]
    ),
    DummyUser(
        'htwooh',
        'Saul',
        'Kripke',
        [
            'water will always be water',
        ],
        [
            'actuspurus',
            'begriff',
        ]
    ),
    DummyUser(
        'begriff',
        'Gottlob',
        'Frege',
        [
            "I don't give a darn what you think",
        ],
        [
            'actuspurus',
            'hammerfromkoenigsberg',
        ]
    ),
    DummyUser(
        'aquinasfangirl',
        'Elizabeth',
        'Anscombe',
        [
            "don't drop that thought",
        ],
        [
            'actuspurus',
            'begriff',
        ]
    ),
    DummyUser(
        'hammerfromkoenigsberg',
        'Immanuel',
        'Kant',
        [
            "I'm a what?",
        ],
        [
            'constantconjunction',
            'hungrymonad',
        ]
    ),
    DummyUser(
        'luckylocke',
        'John',
        'Locke',
        [
            '#medschoolstinks',
        ],
        [
            'cogitus',
            'one',
        ]
    ),
    DummyUser(
        'philophreak',
        'Thomas',
        'Smith',
        [
            "ready for my philo class, it's #popping",
            "who else things @one is the greatest?!",
            "dark caves scare me",
        ],
        [
            'cogitus',
            'one',
            'constantconjunction',
            'actuspurus',
            'hungrymonad',
            'htwooh',
            'begriff',
            'aquinasfangirl',
            'hammerfromkoenigsberg',
            'luckylocke',
        ]
    ),
]

# create Profiles (and the Users they contain) and their Kools
for philo in philos:
    my_user = User(
        username = philo.username,
        password = 'koolack_unscaled',
        first_name = philo.first_name,
        last_name = philo.last_name,
        email = 'jrichels+' + philo.username + '@nd.edu',
    )
    my_user.save()

    my_prof = Profile(user=my_user)
    my_prof.save()

    for kool_contents in philo.kool_contentses:
        my_prof.kool_set.create(contents=kool_contents)

# make Profiles follow one another (all Profiles must be created first)
for philo in philos:
    my_prof = Profile.objects.get(user__username=philo.username)
    
    for follows_username in philo.follows_usernames:
        my_prof.follows.add(Profile.objects.get(user__username=follows_username))
