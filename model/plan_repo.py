from model.plan_parser import parse_plan_json
import hashlib


class PlanRepo():
    def __init__(self, in_redis):
        self.__redis = in_redis

    def reset_id(self):
        self.__redis.set("global_plan_id", 0)

    def get_id(self):
        raw_plan_id = self.__redis.incr("global_plan_id")
        return hashlib.md5(str(raw_plan_id)).hexdigest()

    def save_new_plan(self, plan):
        plan.set_plan_as_new()

        key = plan.get_plan_id()

        if key is None:
            key = self.get_id()
            plan.set_plan_id(key)

        self.__redis.set("plan-{}".format(key), plan.to_json())
        return key

    def purge_all_plans(self):
        keys = self.__get_all_redis_keys()
        map(lambda key: self.__redis.delete(key), keys)

    def get_plan_by_id(self, plan_id):
        redis_plan_json = self.__redis.get("plan-{}".format(plan_id))
        return parse_plan_json(redis_plan_json)

    def get_number_of_plans(self):
        return len(self.__get_all_redis_keys())

    def __get_all_redis_keys(self):
        return self.__redis.keys("plan-*")
