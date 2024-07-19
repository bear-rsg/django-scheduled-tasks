"""Example test case."""
from django.test import TestCase


class FakeTestCase(TestCase):
    """Example test case."""

    def test_fake(self):
        """Test method to validate a 'fake' assertion."""
        self.assertEqual(1, 1)
