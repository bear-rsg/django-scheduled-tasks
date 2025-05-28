"""Database models for scheduled tasks."""
import importlib
import logging
from threading import Lock
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
    next_expected_start_time = models.DateTimeField(null=True)

    _exclusive_lock = Lock()

    def __str__(self):
        """Nice human-readable description of the task."""
        return f"Run {self.func} every {self.interval_minutes} minutes ({'enabled' if self.enabled else 'disabled'})"

    def execute(self):
        """Execute this task."""
        modulename, funcname = self.func.rsplit('.', 1)

        ok = False
        log = ScheduledTaskLog()
        log.scheduled_task = self
        log.start_time = timezone.now()
        log.save()
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
            log.end_time = timezone.now()
            log.success = ok
            log.save()
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

    @property
    def last_end_time(self):
        """Return the end time from the latest ScheduledTaskLog for this ScheduledTask."""
        last_log = self.scheduledtasklog_set.order_by('-end_time').first()
        if last_log and last_log.end_time:
            return last_log.end_time
        return None


class ScheduledTaskLog(models.Model):
    """A record of every time the job has run.

    See the _admin_task() in scheduler.py which cleans up old ScheduledTaskLog records.
    """

    scheduled_task = models.ForeignKey(ScheduledTask, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    success = models.BooleanField(null=True)
