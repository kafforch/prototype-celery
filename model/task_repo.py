import json
from model.plan_parser import TaskParserDeco, DependencyParserDeco


class TaskRepo():
    def __init__(self, in_redis):
        self.__redis = in_redis

    def save_new_tasks(self, plan_id, tasks):
        for task in tasks:
            task.set_task_as_new()
            self.__redis.rpush("tasksof-{}".format(plan_id), task.to_json())

    def save_dependencies(self, plan_id, dependencies):
        for dep in dependencies:
            self.__redis.rpush("dependenciesof-{}".format(plan_id), dep.to_json())

    def purge_all_tasks(self):
        keys = self.__redis.keys("tasksof-*")
        map(lambda key: self.__redis.delete(key), keys)

    def purge_all_dependencies(self):
        keys = self.__redis.keys("dependenciesof-*")
        map(lambda key: self.__redis.delete(key), keys)

    def get_tasks(self, plan_id):
        return map(lambda t: TaskParserDeco(json.loads(t)), \
                   self.__redis.lrange("tasksof-{}".format(plan_id), 0, -1))

    def get_dependencies(self, plan_id):
        return map(lambda t: DependencyParserDeco(json.loads(t)), \
                   self.__redis.lrange("dependenciesof-{}".format(plan_id), 0, -1))

    def get_number_of_tasks(self, plan_id):
        return len(self.get_tasks(plan_id))

    def get_number_of_dependencies(self, plan_id):
        return len(self.get_dependencies(plan_id))

    def save_task(self, plan_id, task):
        tasks = self.get_tasks(plan_id)
        task_ids = map(lambda t: t.get_task_id(), tasks)
        index = None

        try:
            index = task_ids.index(task.get_task_id())
        except:
            return None

        self.__redis.lset("tasksof-{}".format(plan_id), index, task.to_json())
        return index

    def get_task(self, plan_id, task_id):
        tasks = self.get_tasks(plan_id)
        for task in tasks:
            if task.get_task_id() == task_id:
                return task

        return None