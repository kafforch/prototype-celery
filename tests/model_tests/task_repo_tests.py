import unittest
from model import task_repo


class DummyTask:
    def __init__(self, plan_id, task_id):
        self.plan_id = plan_id
        self.task_id = task_id

    def get_plan_id(self):
        return self.plan_id

    def get_task_id(self):
        return self.task_id


class PlanRepoTests(unittest.TestCase):
    def setUp(self):
        task_repo.purge_all_tasks()
        task1 = DummyTask(1,1)
        task2 = DummyTask(1,2)
        task3 = DummyTask(1,3)
        task4 = DummyTask(2,1)
        task5 = DummyTask(2,2)
        task6 = DummyTask(3,1)
        task_repo.save(task5)
        task_repo.save(task3)
        task_repo.save(task1)
        task_repo.save(task2)
        task_repo.save(task4)
        task_repo.save(task6)

    def test_get_by_id_success(self):
        self.assertIsInstance(task_repo.get_by_id(1,2), DummyTask)
        self.assertIsInstance(task_repo.get_by_id(3,1), DummyTask)

    def test_get_by_id_failure(self):
        self.assertIsNone(task_repo.get_by_id(44,33))

    def test_get_number_of_plans(self):
        self.assertEqual(task_repo.get_number_of_tasks(), 6)
