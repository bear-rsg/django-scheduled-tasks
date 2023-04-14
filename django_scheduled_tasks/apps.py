"""Configure this django app."""
import logging
import sys
from django.apps import AppConfig
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


skip_if_arg = set(['migrate', 'test', 'makemigrations'])


class GeneralConfig(AppConfig):
    """Django app config for the 'general' app."""

    name = 'django_scheduled_tasks'

    def ready(self):
        """Start the background scheduler once the app is ready."""
        if set(sys.argv) & skip_if_arg:
            logger.info("Skipping task loading")
            return

        from .models import ScheduledTask
        from .scheduler import start_scheduler
        try:
            tasks = ScheduledTask.objects.filter(enabled=True)
            if tasks:
                start_scheduler()
            else:
                logging.info("No scheduled tasks found - refusing to run the scheduler")
        except OperationalError:
            logging.warning("Can't find ScheduledTask table, please run migrations")
            return
