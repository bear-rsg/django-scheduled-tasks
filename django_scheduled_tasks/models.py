"""Database models for scheduled tasks."""
import importlib
import logging
from threading import Lock
import time
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


logger = logging.getLogger(__name__)


class ScheduledTask(models.Model):
    """A record represents a single scheduled (recurring) task."""

    func = models.CharField(max_length=100, unique=True)  # importable function name
    interval_minutes = models.IntegerField(validators=[MinValueValidator(1),
                                                       MaxValueValidator(1440)])  # 1 min to 24 hours
    onstart = models.BooleanField(default=False)  # run at django startup?
    enabled = models.BooleanField(default=True)
    exclusive = models.BooleanField(default=True)  # run as the only task (I.e. thread locked)
    last_timestamp = models.DateTimeField(null=True, blank=True)
    last_success = models.BooleanField(null=True, blank=True)
    last_runtime = models.FloatField(null=True, blank=True)

    _exclusive_lock = Lock()

    def execute(self):
        """Execute this task."""
        modulename, funcname = self.func.rsplit('.', 1)

        ok = False
        start = time.time()
        try:
            if self.exclusive:
                logger.debug("Getting exclusive scheduled tasks lock for %s", self.func)
                self._exclusive_lock.acquire()
                logger.debug("Getting exclusive scheduled tasks lock for %s", self.func)

            module = importlib.import_module(modulename)
            func = getattr(module, funcname)
            logger.debug("Executing %s", self.func)
            func()
            ok = True
        finally:
            self.last_runtime = time.time() - start
            self.last_timestamp = timezone.now()
            self.last_success = ok
            self.save(reload_scheduler=False)
            if self.exclusive:
                self._exclusive_lock.release()
                logger.debug("Released exclusive scheduled tasks lock for %s", self.func)

    def save(self, *args, reload_scheduler=True, **kwargs):
        """Save the model, and reload the scheduler."""
        super().save(*args, **kwargs)
        if reload_scheduler:
            from .scheduler import reload_scheduler
            reload_scheduler()

    def __str__(self):
        """Nice human-readable description of the task."""
        return f"Run {self.func} every {self.interval_minutes} minutes ({'enabled' if self.enabled else 'disabled'})"
