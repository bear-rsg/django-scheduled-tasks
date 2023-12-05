"""Database models for scheduled tasks."""
import importlib
import logging
import time
from django.utils import timezone
from django.db import connection, models
from django.core.validators import MinValueValidator, MaxValueValidator


logger = logging.getLogger(__name__)


class ScheduledTask(models.Model):
    """A record represents a single scheduled (recurring) task."""

    func = models.CharField(max_length=100, unique=True)  # importable function name
    interval_minutes = models.IntegerField(validators=[MinValueValidator(1),
                                                       MaxValueValidator(1440)])  # 1 min to 24 hours
    onstart = models.BooleanField(default=False)  # run at django startup?
    enabled = models.BooleanField(default=True)
    last_timestamp = models.DateTimeField(null=True, blank=True)
    last_success = models.BooleanField(null=True, blank=True)
    last_runtime = models.FloatField(null=True, blank=True)

    def execute(self):
        """Execute this task."""
        modulename, funcname = self.func.rsplit('.', 1)

        ok = False
        start = time.time()
        try:
            module = importlib.import_module(modulename)
            func = getattr(module, funcname)
            logger.debug("Executing %s", self.func)
            func()
            ok = True
        finally:
            # Close the DB connection so that Django will reconnect it to for the save below
            # This works around the case where the connection has died or timed out before the scheduled task completes
            connection.close_if_unusable_or_obsolete()
            self.last_runtime = time.time() - start
            self.last_timestamp = timezone.now()
            self.last_success = ok
            self.save(reload_scheduler=False)

    def save(self, *args, reload_scheduler=True, **kwargs):
        """Save the model, and reload the scheduler."""
        super().save(*args, **kwargs)
        if reload_scheduler:
            from .scheduler import reload_scheduler
            reload_scheduler()

    def __str__(self):
        """Nice human-readable description of the task."""
        return f"Run {self.func} every {self.interval_minutes} minutes ({'enabled' if self.enabled else 'disabled'})"
