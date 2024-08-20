"""Example test case."""
from django.test import TestCase
from django_scheduled_tasks.models import ScheduledTask
from unittest.mock import patch


def test_func():
    """If the test is correctly executed, it will then pass as True."""
    pass


class ScheduledTaskCase(TestCase):
    """Example test case, testing the three functions (execute, str, save) in the Models module."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.t1 = ScheduledTask.objects.create(
            func='django_scheduled_tasks.tests.test_models.test_func',
            interval_minutes=10
        )

    def test_str(self):
        """Inserting the test obj into the answer string and seeing if it equals the same as the real result."""
        self.assertEqual(
            str(self.t1),
            f"Run {self.t1.func} every {self.t1.interval_minutes} minutes"
            f" ({'enabled' if self.t1.enabled else 'disabled'})"
        )

    @patch('django_scheduled_tasks.tests.test_models.test_func')
    def test_execute(self, mock_test_func):
        """Runs the execute function and changes IS_EXECUTED to True when ran correctly."""
        self.t1.execute()
        mock_test_func.assert_called_once()
