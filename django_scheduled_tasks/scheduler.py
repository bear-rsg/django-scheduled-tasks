import os
from apscheduler.schedulers.background import BackgroundScheduler
from .models import ScheduledTask

_scheduler = BackgroundScheduler()


def start_scheduler():
    """ Start our background scheduler """
    if not os.environ.get('RUN_MAIN'):
        # Not in the main thread - probably running under the development runserver
        return

    _scheduler.start()
    print("Started background scheduler")
    _load_tasks()


def reload_scheduler():
    """ Reload our background scheduler """
    _scheduler.remove_all_jobs()
    print("Restarted background scheduler")
    _load_tasks()


def add_task(func, minutes):
    """
    Add a task to our scheduler. Call function 'func' every 'minutes' minutes.
    """
    _scheduler.add_job(func, 'interval', minutes=minutes)


def _load_tasks():
    """ Load our tasks from the model and add them to the scheduler """
    tasks = ScheduledTask.objects.filter(enabled=True)
    for task in tasks:
        add_task(task.execute, task.interval_minutes)
        print(f"Added task '{task}' to background scheduler")
