__author__ = "corka149"

from pykie.runner import MultiTaskVariables, ProcessRunner
from pykie.core import models
from unittest import TestCase
import unittest


class TestMultiTaskVariables(TestCase):

    def test_matching(self):
        json = {"task-id": 1, "task-name": "CreateShoppingList", "task-created-on": {"java.util.Date": 1539631552.8501}}
        task = models.Task(json)
        mtv = MultiTaskVariables()
        mtv.add_conditional_variables({"name": "Bob"}, id=1)
        mtv.add_conditional_variables({"description": "Lorem ipsum"}, name="ShoppingList")
        mtv.add_conditional_variables({"items": ["Bread", "Apples"]}, name="CreateShoppingList")
        vars = ProcessRunner.__match_variables__(mtv, task)
        self.assertEqual(2, len(vars))


if __name__ == '__main__':
    unittest.main()
