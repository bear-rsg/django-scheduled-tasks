from django.apps import AppConfig
from django.db.utils import OperationalError


class GeneralConfig(AppConfig):
    name = 'django_scheduled_tasks'

    def ready(self):
        from .models import ScheduledTask
        from .scheduler import start_scheduler, add_task

        try:
            tasks = ScheduledTask.objects.filter(enabled=True)
            if tasks:
                start_scheduler()
            else:
                print("No scheduled tasks found - refusing to run the scheduler")
        except OperationalError:
            print("WARNING: Can't find ScheduledTask table, please run migrations")
            return

        for task in tasks:
            add_task(task.execute, task.interval_minutes)
