from .default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/freelance-organizer/db.sqlite3',
    },
}
