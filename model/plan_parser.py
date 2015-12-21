import json


def parse_plan_json(plan_json):
    class DependencyParserDeco:

        def __init__(self, dependency):
            self.__dependency = dependency

        def get_dependency_from(self):
            return self.__dependency["from"]

        def get_dependency_to(self):
            return self.__dependency["to"]

    class TaskParserDeco:

        def __init__(self, task):
            self.__task = task

        def task_get_id(self):
            return self.__task["id"]

        def task_get_name(self):
            return self.__task["name"]

        def is_task_complete(self):
            return "COMPLETE" == self.__task['task_status']

        def is_task_initial(self):
            return "INITIAL" == self.__task['task_status']

        def is_task_running(self):
            return "RUNNING" == self.__task['task_status']

        def set_task_as_complete(self):
            self.__task['task_status'] = "COMPLETE"

        def set_task_as_new(self):
            self.__task['task_status'] = "INITIAL"

        def set_task_as_running(self):
            self.__task['task_status'] = "RUNNING"

        def get_task_id(self):
            return self.__task["id"]

        def get_start_on(self):
            try:
                return self.__task["start_on"]
            except KeyError:
                return None

    class PlanParserDeco:

        def __init__(self):
            self.__plan = json.loads(plan_json)

        def set_plan_id(self, plan_id):
            self.__plan["plan_id"] = plan_id

        def get_plan_id(self):
            return self.__plan["plan_id"]

        def set_plan_as_new(self):
            self.__plan["plan_status"] = "INITIAL"

        def set_plan_as_running(self):
            self.__plan["plan_status"] = "RUNNING"

        def is_plan_initial(self):
            return "INITIAL" == self.__plan["plan_status"]

        def is_plan_running(self):
            return "RUNNING" == self.__plan["plan_status"]

        def get_start_on(self):
            try:
                return self.__plan["start_on"]
            except KeyError:
                return None

        def get_tasks(self):
            return map(lambda task: TaskParserDeco(task), self.__plan["tasks"])

        def set_plan_as_complete(self):
            self.__plan["plan_status"] = "COMPLETE"

        def is_plan_complete(self):
            return "COMPLETE" == self.__plan["plan_status"]

        def get_dependencies(self):
            return map(lambda d: DependencyParserDeco(d), self.__plan["dependencies"])

    return PlanParserDeco()
