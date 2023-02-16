"""
Register tasks for the background scheduler.

This module provides a register_task decorator which can be used to register
callable objects as background tasks. It adds them to the model, if they don't
already exist.
"""
from .models import ScheduledTask
from django.db import IntegrityError


def register_task(interval):
    """
    Register a scheduled task via this decorator.

    Re-registering an existing task does nothing.
    """
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
