#!/usr/bin/env python

import sys
import django

from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'django_scheduled_tasks',
    ),
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'dummy'}},
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
)

django.setup()
call_command('makemigrations', 'django_scheduled_tasks')
