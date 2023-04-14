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
        if set(sys.argv) & skip_if_arg:
            logger.info("Skipping task loading")
            return

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
