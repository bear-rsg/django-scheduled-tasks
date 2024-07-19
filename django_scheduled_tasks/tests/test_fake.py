from django.test import TestCase


class FakeTestCase(TestCase):

    def test_fake(self):
        self.assertEqual(1, 1)
