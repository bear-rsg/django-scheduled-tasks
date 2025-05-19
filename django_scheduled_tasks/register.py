"""
Register tasks for the background scheduler.

This module provides a register_task decorator which can be used to register
callable objects as background tasks. It adds them to the model, if they don't
already exist.
"""
import logging
import sys
from .models import ScheduledTask
from django.db import IntegrityError
from django.conf import settings
from .apps import skip_if_arg

logger = logging.getLogger(__name__)


def register_task(interval, onstart=False):
    """
    Register a scheduled task via this decorator.

    Re-registering an existing task does nothing.

    @param interval: (int) interval between runs, in minutes.
    @param onstart: (bool) should this be run at startup?
    """
    def wrapper(func):
        if getattr(settings, 'DISABLE_SCHEDULED_TASKS', None) is True:
            logger.info("DISABLE_SCHEDULED_TASKS=True - skipping task loading")
            return

        skipped_args = set(sys.argv) & skip_if_arg
        if skipped_args:
            logger.info("Skipping task loading due to arg(s): %s", skipped_args)
            return func

        desc = f'{func.__module__}.{func.__name__}'
        try:
            ScheduledTask.objects.create(func=desc, interval_minutes=interval, onstart=onstart)
        except IntegrityError:
            # update task parameters if they have changed
            obj = ScheduledTask.objects.get(func=desc)
            if interval != obj.interval_minutes or onstart != obj.onstart:
                obj.interval_minutes = interval
                obj.onstart = onstart
                obj.save(update_fields=['interval_minutes', 'onstart'])
        else:
            logging.info(f"Registered scheduled task {desc}")

        return func
    return wrapper
