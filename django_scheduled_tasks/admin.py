"""Register and configure our app for the admin dashboard."""
from django.contrib import admin
from .models import ScheduledTask


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    """Configure some readonly-fields, that are auto-updated."""

    readonly_fields = ('func', 'last_timestamp', 'last_success')
