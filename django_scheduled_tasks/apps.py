"""Configure this django app."""
from django.apps import AppConfig
from django.db.utils import OperationalError


class GeneralConfig(AppConfig):
    """Django app config for the 'general' app."""

    name = 'django_scheduled_tasks'

    def ready(self):
        """Start the background scheduler once the app is ready."""
        from .models import ScheduledTask
        from .scheduler import start_scheduler
        try:
            tasks = ScheduledTask.objects.filter(enabled=True)
            if tasks:
                start_scheduler()
            else:
                print("No scheduled tasks found - refusing to run the scheduler")
        except OperationalError:
            print("WARNING: Can't find ScheduledTask table, please run migrations")
            return
