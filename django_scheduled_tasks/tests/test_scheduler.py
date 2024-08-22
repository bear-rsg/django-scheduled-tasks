"""Example test case."""
from django.test import TestCase
from django_scheduled_tasks.scheduler import start_scheduler, reload_scheduler
from django_scheduled_tasks.models import ScheduledTask
from unittest.mock import patch, MagicMock


def test_func():
    """Dummy test function."""
    pass

class SchedulerTester(TestCase):
    """Tests for BackgroundSchedule object."""
    @patch('django_scheduled_tasks.scheduler._scheduler', new_callable=MagicMock)
    @patch.dict('os.environ', {'UWSGI_ORIGINAL_PROC_NAME': '1'}, clear=True)
    def test_start_scheduler(self, mock_scheduler):
        """Tests that the background scheduler runs."""
        start_scheduler()
        mock_scheduler.start.assert_called_once()

    @patch('django_scheduled_tasks.scheduler._scheduler', new_callable=MagicMock)
    def test_reload_scheduler(self, mock_scheduler):
        """Sets up test data and reloads background scheduler."""
        ScheduledTask.objects.create(
            func='django_scheduled_task.tests.test_scheduler.dummy', 
            interval_minutes=1)
        reload_scheduler()

        mock_scheduler.add_job.assert_called_with(
            ScheduledTask.objects.first().execute, 'interval',
            minutes=1, next_run_time=None
        )
