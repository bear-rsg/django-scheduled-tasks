"""
Background scheduler.

This module contains functions to control the background scheduler, starting it or
reloading it. Doing either will load the tasks from the model into the scheduler.
"""
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from .models import ScheduledTask

logger = logging.getLogger(__name__)

_scheduler = BackgroundScheduler()


def start_scheduler():
    """Start our background scheduler."""
    if not (os.environ.get('UWSGI_ORIGINAL_PROC_NAME') or os.environ.get('RUN_MAIN')):
        # UWSGI_ORIGINAL_PROC_NAME => we're running under uwsgi
        # RUN_MAIN => we're in the development server, and the main process
        # Otherwise, don't start the scheduler.
        return

    _scheduler.start()
    logging.info("Started background scheduler")
    _load_tasks()


def reload_scheduler():
    """Reload our background scheduler."""
    _scheduler.remove_all_jobs()
    logging.info("Restarted background scheduler")
    _load_tasks()


def add_task(func, minutes):
    """Add a task to our scheduler. Call function 'func' every 'minutes' minutes."""
    _scheduler.add_job(func, 'interval', minutes=minutes)


def _load_tasks():
    """Load our tasks from the model and add them to the scheduler."""
    tasks = ScheduledTask.objects.filter(enabled=True)
    for task in tasks:
        add_task(task.execute, task.interval_minutes)
        logging.info(f"Added task '{task}' to background scheduler")
