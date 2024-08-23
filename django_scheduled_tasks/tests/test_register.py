"""Example test case."""
from django_scheduled_tasks.models import ScheduledTask
from django_scheduled_tasks.register import register_task
from django.test import TestCase
from unittest.mock import patch


class RegisterTaskTest(TestCase):
    """Test case for the `register_task` wrapper."""

    def test_register_task(self):
        """Checks that the register is empty, and then creates an object."""
        self.assertFalse(ScheduledTask.objects.all().exists())

        @register_task(1)
        def dummy():
            pass

        self.assertEqual(ScheduledTask.objects.count(), 1)
        st = ScheduledTask.objects.first()
        self.assertEqual(st.func, "django_scheduled_tasks.tests.test_register.dummy")

    @patch('django_scheduled_tasks.register.settings', DISABLE_SCHEDULED_TASKS=True)
    def test_register_task_with_disable_register_task(self, mock_settings):
        """Tests that disabling in settings correctly stops a task form being registered."""
        @register_task(1)
        def dummy():
            pass

        self.assertFalse(ScheduledTask.objects.all().exists())

    @patch('django_scheduled_tasks.register.sys', argv=['test'])
    def test_resgister_task_with_skipped_args(self, mock_sys_arg):
        """Tests that running with `test` argument stops a task form being registered."""
        @register_task(1)
        def dummy():
            pass

        self.assertFalse(ScheduledTask.objects.all().exists())


class SpecificScheduledTaskTest(TestCase):
    """Testing the schedule_task function."""

    @classmethod
    def setUpTestData(cls):
        cls.func = 'django_scheduled_tasks.tests.test_models.test_func'

    @patch('django_scheduled_tasks.models.ScheduledTask.objects.create')
    def test_schedule_task_with_invalid_day(self, mock_create):
        with self.assertRaises(ValueError):
            schedule_task(day=-1, hour=12)

    def test_schedule_task_correct(self):
        if day is not None and (day < 0 or day > 6):
            raise ValueError("Day must be between 0 (Monday) and 6 (Sunday)")

        if hour is not None and (hour < 0 or hour > 23):
            raise ValueError("Hour must be between 0 and 23")
