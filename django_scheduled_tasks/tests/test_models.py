"""Test for django_scheduled_tasks.models."""
from django.test import TestCase
from django_scheduled_tasks.models import ScheduledTask
from unittest.mock import patch


def test_func():
    """Dummy test function."""
    pass


class ScheduledTaskCase(TestCase):
    """Tests for ScheduledTask model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.t1 = ScheduledTask.objects.create(
            func='django_scheduled_tasks.tests.test_models.test_func',
            interval_minutes=10
        )

    def test_str(self):
        """Test the str dunder method."""
        self.assertEqual(
            str(self.t1),
            f"Run {self.t1.func} every {self.t1.interval_minutes} minutes"
            f" ({'enabled' if self.t1.enabled else 'disabled'})"
        )

    @patch('django_scheduled_tasks.tests.test_models.test_func')
    def test_execute(self, mock_test_func):
        """Test that the execute method runs an instance of the dummy function."""
        self.t1.execute()
        mock_test_func.assert_called_once()
