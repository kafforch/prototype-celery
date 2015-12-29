from workers.plan_submitter import PlanSubmitter
from unittest import TestCase
from model.plan_parser import parse_plan_json
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from redis import Redis

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
                },
                {
                    "id": "27",
                    "start_on": "2026-12-11T23:14:15.554Z",
                    "name": "namename123"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                },
                {
                    "from": "2",
                    "to": "3"
                }
            ]
            }'''



class LiveTest(TestCase):

    def setUp(self):
        self.ps = PlanSubmitter(
            "localhost"
        )

    def test_live1(self):
        plan_repo = PlanRepo(Redis("localhost"))

        plan = parse_plan_json(plan_json1)
        result = self.ps.store_plan.delay(plan)

        plan_id = result.get(5)

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 3)