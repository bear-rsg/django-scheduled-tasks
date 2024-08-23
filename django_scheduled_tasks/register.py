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


DEFAULT_SCHEDULE_HOUR = 2


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

        try:
            desc = f'{func.__module__}.{func.__name__}'
            ScheduledTask.objects.create(func=desc, interval_minutes=interval, onstart=onstart)
        except IntegrityError:
            # Already registered
            pass
        else:
            logging.info(f"Registered scheduled task {desc}")

        return func
    return wrapper


def schedule_task(day, hour=DEFAULT_SCHEDULE_HOUR, onstart=False):
    """Add a scheduled task for a specific day of the week.

    Args:
         day (int): Day of the week, indexing from 0 in Monday.
         hour (int, optional): Hour of the day, 24-hour clock, defaults to `DEFAULT_SCHEDULE_HOUR`.
         onstart (bool, optional): Should this be run at startup, defaults to `False`.
    """
    pass
