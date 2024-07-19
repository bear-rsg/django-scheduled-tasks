#!/usr/bin/env python
import sys
import os

import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import call_command


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "django_scheduled_tasks")
TEST_DIR = os.path.join(APP_DIR, "tests")

if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        USE_TZ = True,
        DATABASES = {
            "default": {
                "NAME": os.path.join(APP_DIR, 'django_scheduled_tasks.sqlite3'),
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS = [
            "django_scheduled_tasks",
        ],
        NOSE_ARGS=["-s"],
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    )

    django.setup()

    TestRunner = get_runner(settings)
    runner = TestRunner()

    sys.exit(
        bool(runner.run_tests([]))
    )
