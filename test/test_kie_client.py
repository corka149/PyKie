__author__ = "corka149"

from pykie.core import KieClient, KieServerUnavailableError
from unittest import TestCase
from requests import codes
import unittest

container = "py-kie-tes_1.0.0"
process_def = "CreatingBuyingList"
auth = ("admin", "admin")
correct_server_address = "127.0.0.1:8180"


class TestKieClient(TestCase):

    def test_successful_bootstrap_client(self):
        KieClient(correct_server_address, auth)
        self.assertTrue(True)

    def test_unsuccessful_bootstrap_client(self):
        with self.assertRaises(KieServerUnavailableError):
            KieClient("127.0.0.1:8181", auth)
            
    def test_start_process_instance(self):
        kc = KieClient(correct_server_address, auth)
        p_vars = {"buyer": "admin", "budget": 222.55, "shop": "SuperBuy", "onlyFood": False}
        status_code, id = kc.start_process(container, process_def, p_vars)
        self.assertEqual(status_code, codes.created)
        self.assertTrue(id > 0)

    def test_complete_task(self):
        kc = KieClient(correct_server_address, auth)
        p_vars = {"buyer": "admin", "budget": 123.4, "shop": "SuperBuy", "onlyFood": True}
        _, process_id = kc.start_process(container, "CreatingBuyingList", p_vars)
        tasks = kc.get_tasks_by_instance(process_id)
        self.assertEqual(len(tasks), 1)
        items = {"items": {"bread": 1, "apple": 5, "sausage": 3}}
        resp = kc.complete_task(container, tasks[0].id, items)
        self.assertEqual(resp, codes.created)


if __name__ == '__main__':
    unittest.main()
