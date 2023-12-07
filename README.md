# Django scheduled tasks app

Django app for running/monitoring/enabling/disabling scheduled background tasks.

This uses the apscheduler library, and doesn't require any additional services.

## Installation

Include the library in your requirements.txt (or equivalent):

```
git+https://github.com/bear-rsg/django-scheduled-tasks.git
```

Add the app to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    'django_scheduled_tasks',
]
```

Define your scheduled tasks (e.g. scheduled_tasks.py)

```
from django_scheduled_tasks.register import register_task

@register_task(interval=1)
def test_task():
    print("I am the test task")
```

Load the tasks when your app starts (apps.py):

```
import sys
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        """ Import our scheduled tasks module, which will register the tasks with the scheduler """
        if 'migrate' not in sys.argv:
            from . import scheduled_tasks

```

If you're running under uwsgi, then you'll need to add this to your uwsgi.ini:

```
enable-threads = true
```

If you are running code that includes django_scheduled_tasks, but want to disable the tasks globally, then configure
this in settings.py:
```
DISABLE_SCHEDULED_TASKS = True
```

If you experience a lost DB connection with a scheduled task then add
```python
from django.db import connection
connection.close_if_unusable_or_obsolete()
```
to reset the connection.
