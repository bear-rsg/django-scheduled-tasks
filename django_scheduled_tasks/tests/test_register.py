from django_scheduled_tasks.models import ScheduledTask
from django_scheduled_tasks.register import register_task
from django.test import TestCase
from unittest.mock import patch


class RegisterTaskTest(TestCase):
    """Example test case, testing the wrapper function."""

    def test_wrapper(self):
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
        """Uses settings to disable scheduled tasks."""
        @register_task(1)
        def dummy():
            pass

        self.assertFalse(ScheduledTask.objects.all().exists())

    @patch('django_scheduled_tasks.register.sys', argv=['test'])
    def test_resgister_task_with_skipped_args(self, mock_sys_arg):
        """Uses system to skip task."""
        @register_task(1)
        def dummy():
            pass

        self.assertFalse(ScheduledTask.objects.all().exists())

    # @Mock('django_scheduled_tasks.tests.test_register.dummy', side_effect=)
    # def test_integrity(self):

    #     @register_task(1)
    #     def dummy():
    #         pass

    #     @register_task(1)
    #     def dummy():
    #         pass

        '''self.assertEqual(ScheduledTask.objects.count(), 1)

        st = ScheduledTask.objects.first()
        self.assertEqual(st.func, "django_scheduled_tasks.tests.test_register.dummy")'''
