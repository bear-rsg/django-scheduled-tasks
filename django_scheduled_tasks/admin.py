from django.contrib import admin
from .models import ScheduledTask


class ScheduledTaskAdmin(admin.ModelAdmin):
    readonly_fields=('last_timestamp', 'last_success')


admin.site.register(ScheduledTask, ScheduledTaskAdmin)
