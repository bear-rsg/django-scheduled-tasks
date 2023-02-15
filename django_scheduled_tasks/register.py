from .models import ScheduledTask
from django.db import IntegrityError


def register_task(interval):
    def wrapper(func):
        try:
            desc = f'{func.__module__}.{func.__name__}'
            ScheduledTask.objects.create(func=desc, interval_minutes=interval)
        except IntegrityError:
            # Already registered
            pass
        else:
            print(f"Registered scheduled task {desc}")
        return func
    return wrapper
