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


class DummyDependency:
    def __init__(self, _from, _to):
        self._from = _from
        self._to = _to

    def get_from(self):
        return self._from

    def get_to(self):
        return self._to


class TaskRepoTests(unittest.TestCase):
    def setUp(self):
        task_repo.purge_all_tasks()
        task_repo.purge_all_dependencies()
        task1 = DummyTask(1,1)
        task2 = DummyTask(1,2)
        task3 = DummyTask(1,3)
        task4 = DummyTask(2,1)
        task5 = DummyTask(2,2)
        task6 = DummyTask(3,1)
        task_repo.save_tasks(1, [task1, task2, task3])
        task_repo.save_tasks(2, [task4, task5])
        task_repo.save_tasks(3, [task6])

        dep1 = DummyDependency(1,2)
        dep2 = DummyDependency(2,3)
        dep3 = DummyDependency(3,4)
        dep4 = DummyDependency(4,4)
        dep5 = DummyDependency(5,6)

        task_repo.save_dependencies(1, [dep1, dep2])
        task_repo.save_dependencies(2, [dep3, dep4])
        task_repo.save_dependencies(3, [dep5])


    def test_get_by_id_success(self):
        self.assertIsInstance(task_repo.get_task_by_id(1,2), DummyTask)
        self.assertIsInstance(task_repo.get_task_by_id(3,1), DummyTask)
        self.assertIsInstance(task_repo.get_dependency(1,1,2), DummyDependency)

    def test_get_by_id_failure(self):
        self.assertIsNone(task_repo.get_task_by_id(44,33))
        self.assertIsNone(task_repo.get_dependency(66,77,88))

    def test_get_number_of_plans(self):
        self.assertEqual(task_repo.get_number_of_tasks(), 6)
        self.assertEqual(task_repo.get_number_of_dependencies(), 5)
