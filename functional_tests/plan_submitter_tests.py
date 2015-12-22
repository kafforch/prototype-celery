from workers import plan_submitter
from model import plan_parser

import unittest

plan_json1 = '''{
            "start_on": "2015-12-11T23:14:15.554Z",
            "tasks": [
                {
                    "id": "1",
                    "name": "task1",
                    "test": "test123"
                },
                {
                    "id": "23",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                }
            ]
            }'''

class PlanSubmitterTests(unittest.TestCase):

    def test_plan_submission1(self):
        plan = plan_parser.parse_plan_json(plan_json1)
        plan_id = plan_submitter.store_plan.delay(plan)

        self.assertIsNotNone(plan_id)