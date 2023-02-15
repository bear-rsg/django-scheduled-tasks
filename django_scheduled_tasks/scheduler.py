from apscheduler.schedulers.background import BackgroundScheduler

_scheduler = BackgroundScheduler()


def start_scheduler():
    """ Start our background scheduler """
    _scheduler.start()


def add_task(func, minutes):
    """
    Add a task to our scheduler. Call function 'func' every 'minutes' minutes.
    """
    _scheduler.add_job(func, 'interval', minutes=minutes)
