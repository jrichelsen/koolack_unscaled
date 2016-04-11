# needed to access Django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koolack_unscaled_proj.settings")
django.setup()

from django.contrib.auth.models import User
from collections import namedtuple

from koolack_unscaled.models import Profile, Kool

DummyUser = namedtuple('DummyUser', ['username', 'first_name', 'last_name', 'kool_contents', 'follows_usernames'])

philos = [
    DummyUser(
        'cogitus',
        'Rene',
        'Descarte',
        [
            'I think, I am.',
            'had a great weekend in #Munich',
            '@aristotle wrong again on those motion laws #galileo',
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
            'another day grinding the lances #dailygrind',
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
            'just got a new #turban',
            "@lonelyidealist salamanders aren't real",
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
            "just proved God's existence 5 times over #anotherone",
            "reading @aristotle, @cogitus won't understand",
        ],
        []
    ),
    DummyUser(
        'hungrymonad',
        'Gottfried',
        'Leibniz',
        [
            "I'm so strange rn",
            'getting paid to be in Germany #travelstatus',
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
            '#favotitethings are #roses, and#otherthings',
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
    my_user = User(username = philo.username,
        first_name = philo.first_name,
        last_name = philo.last_name)
    my_user.set_password('koolack_unscaled')
    my_user.save()

    my_prof = Profile(user=my_user)
    my_prof.save()

    for kool_content in philo.kool_contents:
        my_user.kool_set.create(content=kool_content)

# make Profiles follow one another (all Profiles must be created first)
for philo in philos:
    my_prof = Profile.objects.get(user__username=philo.username)
    
    for follows_username in philo.follows_usernames:
        my_prof.follows.add(Profile.objects.get(user__username=follows_username))
