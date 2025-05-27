"""
Background scheduler.

This module contains functions to control the background scheduler, starting it or
reloading it. Doing either will load the tasks from the model into the scheduler.
"""
from datetime import datetime, timedelta
import logging
import os
from threading import Lock
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


def add_task(func, minutes, next_run_time):
    """Add a task to our scheduler. Call function 'func' every 'minutes' minutes."""
    _scheduler.add_job(func, 'interval', minutes=minutes, next_run_time=next_run_time)


def _load_tasks():
    """Load our tasks from the model and add them to the scheduler."""
    tasks = ScheduledTask.objects.filter(enabled=True)

    # If onstart=True then we launch the task (almost) straight away. The one minute delay here
    # is to allow the main program to start (e.g. django) and not interfere with its thread launching.
    soon = datetime.now() + timedelta(minutes=1)

    for task in tasks:
        add_task(task.execute, task.interval_minutes, next_run_time=soon if task.onstart else None)
        logging.info(f"Added task '{task}' to background scheduler")

    add_task(_status_task, 1, datetime.now())
    logging.info(f"Added status task to background scheduler")


def _status_task():
    """Update the status of tasks in django db from info on the jobs."""
    for job in _scheduler.get_jobs():
        if hasattr(job.func, '__self__'):
            obj = job.func.__self__  # a ScheduledTask object
            if obj.next_expected_start_time != job.next_run_time:
                obj.next_expected_start_time = job.next_run_time
                obj.save(reload_scheduler=False)
                logger.debug("Updated job %s next run time to %s", job.func.__self__.func, job.next_run_time)

    logger.info("Status task complete")

