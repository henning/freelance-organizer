from .default import *

DATA_DIR="/var/lib/freelance-organizer/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/freelance-organizer/db.sqlite3',
    },
}
