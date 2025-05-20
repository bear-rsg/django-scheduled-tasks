"""
Background scheduler.

This module contains functions to control the background scheduler, starting it or
reloading it. Doing either will load the tasks from the model into the scheduler.
"""
from datetime import datetime, timedelta
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
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


def add_task(func, minutes, next_run_time):
    """Add a task to our scheduler. Call function 'func' every 'minutes' minutes."""
    _scheduler.add_job(func, 'interval', minutes=minutes, next_run_time=next_run_time)


def add_day_task(func, day, hour, next_run_time):
    """Add a task to our scheduler. Call function 'func' on every 'day' at 'hour' hours."""
    _scheduler.add_job(func, trigger=CronTrigger(day_of_week=day, hour=hour), next_run_time=next_run_time)


def _load_tasks():
    """Load our tasks from the model and add them to the scheduler."""
    tasks = ScheduledTask.objects.filter(enabled=True)

    # If onstart=True then we launch the task (almost) straight away. The one minute delay here
    # is to allow the main program to start (e.g. django) and not interfere with its thread launching.
    soon = datetime.now() + timedelta(minutes=1)

    for task in tasks:
        if task.interval_minutes:
            add_task(task.execute, task.interval_minutes, next_run_time=soon if task.onstart else None)
        else:
            add_day_task(task.execute, task.day, task.hour, next_run_time=soon if task.onstart else None)

        logging.info(f"Added task '{task}' to background scheduler")
