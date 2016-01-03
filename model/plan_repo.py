from model.plan_parser import parse_plan_json, TaskParserDeco, DependencyParserDeco
from model.redis_lookups import const
import hashlib


class PlanRepo():
    def __init__(self, in_redis):
        self.__redis = in_redis

    def reset_id(self):
        self.__redis.set(const.PLAN_ID_SEED, 0)

    def get_id(self):
        raw_plan_id = self.__redis.incr(const.PLAN_ID_SEED)
        return hashlib.md5(str(raw_plan_id)).hexdigest()

    def save_new_plan(self, plan):
        plan.set_plan_as_new()

        key = plan.get_plan_id()

        if key is None:
            key = self.get_id()
            plan.set_plan_id(key)

        self.save_plan(key, plan)
        return key

    def save_plan(self, key, plan):
        self.__redis.set(const.PLAN_KEY.format(key), plan.to_json())

    def purge_all_plans(self):
        keys = self.__get_all_redis_keys()
        map(lambda key: self.__redis.delete(key), keys)

    def get_plan_by_id(self, plan_id):
        plan_json = self.__redis.get(const.PLAN_KEY.format(plan_id))
        tasks_list = self.__redis.lrange(const.TASKS_OF_PLAN.format(plan_id), 0, -1)
        dependencies_list = self.__redis.lrange(const.DEPENDENCIES_OF_PLAN.format(plan_id), 0, -1)
        plan = parse_plan_json(plan_json)
        plan.set_tasks(tasks_list)
        plan.set_dependencies(dependencies_list)
        return plan

    def get_number_of_plans(self):
        return len(self.__get_all_redis_keys())

    def __get_all_redis_keys(self):
        return self.__redis.keys(const.PLAN_WILDCARD)

    def get_all_plan_ids(self):
        return map(lambda s: s.split(const.PLAN_PREFIX)[1], self.__get_all_redis_keys())
