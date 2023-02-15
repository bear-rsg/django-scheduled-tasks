#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django-scheduled-tasks",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        STATIC_URL='/tmp/',
        DEFAULT_AUTO_FIELD='django.db.models.AutoField'
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["django-scheduled-tasks.tests"])
    sys.exit(bool(failures))
