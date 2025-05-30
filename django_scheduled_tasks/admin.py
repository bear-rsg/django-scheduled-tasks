"""Register and configure our app for the admin dashboard."""
from django.contrib import admin
from .models import ScheduledTask, ScheduledTaskLog


class ScheduledTaskLogInline(admin.TabularInline):
    """Inline list for scheduled task logs."""

    model = ScheduledTaskLog
    readonly_fields = ('start_time', 'end_time', 'success')

    def has_add_permission(self, request, obj=None):
        """Disable ability to add ScheduledTaskLog in the admin interface."""
        return False


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    """Configure some readonly-fields, that are auto-updated."""

    readonly_fields = ('func', 'next_expected_start_time')
    inlines = (ScheduledTaskLogInline, )
    list_display = ('func', 'interval_minutes', 'enabled', 'last_end_time', 'next_expected_start_time')

    def has_add_permission(self, request, obj=None):
        """Disable ability to add ScheduledTask in the admin interface."""
        return False
