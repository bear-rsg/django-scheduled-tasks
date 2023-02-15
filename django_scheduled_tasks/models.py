import importlib
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ScheduledTask(models.Model):
    """
    A record represents a single scheduled (recurring) task
    """
    func = models.CharField(max_length=100, unique=True)  # importable function name
    interval_minutes = models.IntegerField(validators=[MinValueValidator(1),
                                                       MaxValueValidator(1440)]) # 1 min to 24 hours
    enabled = models.BooleanField(default=True)
    last_timestamp = models.DateTimeField(null=True, blank=True)
    last_success = models.BooleanField(null=True, blank=True)

    def execute(self):
        """ A callable function, found using our string func value """
        modulename, funcname = self.func.rsplit('.', 1)
        imported_module = importlib.import_module(modulename)
        func = getattr(imported_module, funcname)

        ok = False
        try:
            func()
            ok = True
        finally:
            self.last_timestamp = timezone.now()
            self.last_success = ok
            self.save()

    def __str__(self):
        return f"Run {self.func} every {self.interval_minutes} minutes ({'enabled' if self.enabled else 'disabled'})"
