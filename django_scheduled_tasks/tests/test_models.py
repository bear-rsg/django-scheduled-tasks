"""Example test case."""
from django.test import TestCase
from django_scheduled_tasks.models import ScheduledTask

IS_EXECUTED = False 

def test_func():
    """if the test is correctly executed, it will then pass as True """  
    IS_EXECUTED = True 


class ScheduledTaskCase(TestCase):
    """Example test case, testing the three functions (execute, str, save) in the Models module"""

    @classmethod
    def setUpTestData(cls):
        """ example object being used in each test  """  
        cls.t1 = ScheduledTask.objects.create(
            func='django_scheduled_tasks.tests.test_models.test_func',
            interval_minutes=10
        )

    def test_str(self):
        """ inserting the test obj into the answer string and seeing if it equals the same as the real result """  
        self.assertEqual(
            str(self.t1),
            f"Run {self.t1.func} every {self.t1.interval_minutes} minutes ({'enabled' if self.t1.enabled else 'disabled'})"
        )

    def test_execute(self): 
        """ runs the execute function and changes IS_EXECUTED to True when ran correctly """  

        self.assertFalse(IS_EXECUTED)
        self.t1.execute()
        self.assertTrue(IS_EXECUTED)

    
