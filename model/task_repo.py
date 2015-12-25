import json
from model.plan_parser import TaskParserDeco, DependencyParserDeco

class TaskRepo():
    def __init__(self, in_redis):
        self.__redis = in_redis

    def save_tasks(self, plan_id, tasks):
        for task in tasks:
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
