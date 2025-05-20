"""Example test case."""
from django_scheduled_tasks.models import ScheduledTask
from django_scheduled_tasks.register import register_task, schedule_task
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


class ScheduledTaskTestCase(TestCase):
    """Testing the schedule_task function."""

    def test_schedule_task(self):
        """Test decorator registers task."""
        @schedule_task('mon')
        def dummy():
            pass

        self.assertTrue(ScheduledTask.objects.all().exists())

    def test_schedule_task_with_hour(self):
        """Test decorator registers task with hour argument."""
        @schedule_task('mon', hour=12)
        def dummy():
            pass

        self.assertTrue(ScheduledTask.objects.all().exists())
