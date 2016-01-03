from unittest import TestCase
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from model.plan_parser import parse_plan_json
from model.task_starter_logic import get_tasks_available_to_start
import fakeredis

plan_json1 = '''{
            "start_on": "2007-04-05T12:30-02:00",
            "tasks": [
                {
                    "task_id": "1",
                    "name": "task1",
                    "test": "test123"
                },
                {
                    "task_id": "2",
                    "start_on": "2007-04-05T12:30-02:00",
                    "name": "namename"
                },
                {
                    "task_id": "3",
                    "start_on": "2007-04-05T12:30-02:00",
                    "name": "namename"
                },
                {
                    "task_id": "4",
                    "start_on": "2015-12-11T23:14:15.554Z",
                    "name": "namename"
                },
                {
                    "task_id": "5",
                    "start_on": "2015-12-11T23:14:15.554Z",
                    "name": "namename"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                },
                {
                    "from": "1",
                    "to": "3"
                },
                {
                    "from": "2",
                    "to": "5"
                },
                {
                    "from": "3",
                    "to": "4"
                },
                {
                    "from": "4",
                    "to": "5"
                }
            ]
            }'''

class TaskStarterTests(TestCase):

    def setUp(self):
        self.plan_repo = PlanRepo(fakeredis.FakeStrictRedis())
        self.task_repo = TaskRepo(fakeredis.FakeStrictRedis())

        plan = parse_plan_json(plan_json1)
        plan_id = self.plan_repo.save_new_plan(plan)
        self.task_repo.save_new_tasks(plan_id, plan.get_tasks())
        self.task_repo.save_dependencies(plan_id, plan.get_dependencies())
        self.plan_id = plan_id

    def test_get_tasks(self):

        def assert_task_ids_in_list(actual_tasks_list, assertion_task_id_list):
            self.assertListEqual(
                map(lambda t: t.get_task_id(), actual_tasks_list),
                assertion_task_id_list
            )

        task_list = self.task_repo.get_tasks(self.plan_id)
        dependencies = self.task_repo.get_dependencies(self.plan_id)

        task1 = task_list[0]
        task2 = task_list[1]
        task3 = task_list[2]
        task4 = task_list[3]
        task5 = task_list[4]

        task_list_1 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_1, ["1"])

        task1.set_task_as_complete()
        self.task_repo.save_task(self.plan_id, task1)

        task_list_2 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_2, ["2", "3"])

        task2.set_task_as_complete()
        self.task_repo.save_task(self.plan_id, task2)

        task_list_3 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_3, ["3"])

        task3.set_task_as_complete()
        self.task_repo.save_task(self.plan_id, task3)

        task_list_4 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_4, ["4"])

        task4.set_task_as_complete()
        self.task_repo.save_task(self.plan_id, task4)

        task_list_5 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_5, ["5"])

        task5.set_task_as_complete()
        self.task_repo.save_task(self.plan_id, task5)

        task_list_6 = get_tasks_available_to_start(self.plan_id, task_list, dependencies)
        assert_task_ids_in_list(task_list_6, [])