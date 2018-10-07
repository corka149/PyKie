__author__ = "corka149"

from runner import ProcessRunner
from core import KieClient
from unittest import TestCase
import unittest

container = "py-kie-tes_1.0.0"
process_def = "CreatingBuyingList"
auth = ("admin", "admin")


class TestProcessRunner(TestCase):

    def test_complete_whole_process(self):
        p_vars = {"buyer": "admin", "budget": 222.55, "shop": "SuperBuy", "onlyFood": False}
        kc = KieClient("127.0.0.1:8180", auth)
        pr = ProcessRunner(kc, container, process_def)
        pr.start(p_vars)
        self.assertTrue(pr.process_instance is not None)
        for _ in range(0, 4):
            pr.step(None)
        self.assertTrue(pr.is_done())


if __name__ == '__main__':
    unittest.main()
