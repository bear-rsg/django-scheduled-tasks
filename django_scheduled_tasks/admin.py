from django.contrib import admin
from .models import ScheduledTask


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    readonly_fields = ('last_timestamp', 'last_success')
