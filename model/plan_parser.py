import json


class BaseDeco(object):
    def __init__(self, payload):
        if isinstance(payload, dict):
            self.entity = payload
        elif isinstance(payload, basestring):
            self.entity = json.loads(payload)
        else:
            raise AttributeError("Unknown argument passed to constructor")

    def method_missing(self, attr, *args, **kwargs):
        if attr.startswith("get_"):
            key = attr[len("get_"):]
            if key in self.entity:
                return self.entity[key]
            else:
                return None
        elif attr.startswith("set_"):
            key = attr[len("set_"):]
            self.entity[key] = args[0]
        else:
            raise AttributeError("Missing method %s called." % attr)

    def __getattr__(self, attr, *args, **kwargs):

        if attr.startswith('__') and attr.endswith('__'):
            return super.__getattr__(attr)

        def func(*args, **kwargs):
            return self.method_missing(attr, *args, **kwargs)

        return func


class DependencyParserDeco(BaseDeco):
    def __init__(self, payload):
        super(DependencyParserDeco, self).__init__(payload)

    def to_json(self):
        return json.dumps(self.entity)


class TaskParserDeco(BaseDeco):
    def __init__(self, payload):
        super(TaskParserDeco, self).__init__(payload)

    def is_task_complete(self):
        return "COMPLETE" == self.entity['task_status']

    def is_task_initial(self):
        return "INITIAL" == self.entity['task_status']

    def is_task_running(self):
        return "RUNNING" == self.entity['task_status']

    def set_task_as_complete(self):
        self.entity['task_status'] = "COMPLETE"

    def set_task_as_new(self):
        self.entity['task_status'] = "INITIAL"

    def set_task_as_running(self):
        self.entity['task_status'] = "RUNNING"

    def to_json(self):
        return json.dumps(self.entity)


class PlanParserDeco(BaseDeco):
    def __init__(self, payload):
        super(PlanParserDeco, self).__init__(payload)

    def set_plan_as_new(self):
        self.entity["plan_status"] = "INITIAL"

    def set_plan_as_running(self):
        self.entity["plan_status"] = "RUNNING"

    def is_plan_initial(self):
        return "INITIAL" == self.entity["plan_status"]

    def is_plan_running(self):
        return "RUNNING" == self.entity["plan_status"]

    def get_tasks(self):
        return map(lambda task: TaskParserDeco(task), self.entity["tasks"])

    def set_tasks(self, tasks):
        self.entity["tasks"] = map(lambda t: json.loads(t), tasks)

    def set_plan_as_complete(self):
        self.entity["plan_status"] = "COMPLETE"

    def is_plan_complete(self):
        return "COMPLETE" == self.entity["plan_status"]

    def get_dependencies(self):
        return map(lambda d: DependencyParserDeco(d), self.entity["dependencies"])

    def set_dependencies(self, dependencies):
        self.entity["dependencies"] = map(lambda d: json.loads(d), dependencies)

    def to_json(self):
        return json.dumps(self.entity)


def parse_plan_json(plan_json):
    return PlanParserDeco(plan_json)
