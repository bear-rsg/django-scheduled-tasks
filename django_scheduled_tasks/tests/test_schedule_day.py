"""Example test case."""
from django.test import TestCase
from django_scheduled_tasks.models import ScheduledTask
from django_scheduled_tasks.register import schedule_task
from unittest.mock import patch


def test_func():
    """Dummy test function."""
    pass

class SpecificScheduledTaskTest(TestCase):
    """Testing the schedule_task function."""

    @classmethod
    def setUpTestData(cls):
        cls.func = 'django_scheduled_tasks.tests.test_models.test_func'
        
        
    @patch('django_scheduled_tasks.models.ScheduledTask.objects.create')
    def test_schedule_task_with_invalid_day(self, mock_create):
        with self.assertRaises(ValueError):
            schedule_task(day=-1, hour=12)


    def test_schedule_task_correct(interval=None, onstart=False, day=None, hour=None):
        if day is not None and (day < 0 or day > 6):
            raise ValueError("Day must be between 0 (Monday) and 6 (Sunday)")
        
        if hour is not None and (hour < 0 or hour > 23):
            raise ValueError("Hour must be between 0 and 23")


        

            
        