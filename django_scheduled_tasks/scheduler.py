"""
Background scheduler.

This module contains functions to control the background scheduler, starting it or
reloading it. Doing either will load the tasks from the model into the scheduler.
"""
from datetime import datetime, timedelta
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler

from .models import ScheduledTask

logger = logging.getLogger(__name__)

# Clean up logs older than this (in seconds)
LOG_MAX_AGE = 3 * 24 * 3600

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

    add_task(_admin_task, 1, datetime.now())
    logging.info("Added status task to background scheduler")


def _admin_task():
    """Carry out admin tasks.

    1) Update expected next run time for all jobs, writing it to the ScheduledTask record
    2) Clean up old log records so we don't grow forever
    """
    # Update expected next run time for all jobs
    for job in _scheduler.get_jobs():
        if hasattr(job.func, '__self__'):
            obj = job.func.__self__  # a ScheduledTask object
            if obj.next_expected_start_time != job.next_run_time:
                obj.next_expected_start_time = job.next_run_time
                obj.save(reload_scheduler=False)
                logger.debug("Updated job %s next run time to %s", job.func.__self__.func, job.next_run_time)

    # Clean up old log records so we don't grow forever
    cutoff = datetime.now() - timedelta(seconds=LOG_MAX_AGE)
    for task in ScheduledTask.objects.all():
        # Find old logs based on start time, as sometimes the end time won't be set if the job failed to complete
        old_logs = task.scheduledtasklog_set.filter(start_time__lt=cutoff)
        logger.debug("Deleting %d logs older than %s for task %s", old_logs.count(), cutoff, task.func)
        old_logs.delete()

    logger.info("Admin task complete")
