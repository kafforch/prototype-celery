# Dictionary, where:
#   key: plan_id
#   value: list of associated tasks
class Tasks:
    def __init__(self):
        pass


__t = Tasks()
__t.tasks = {}
__t.dependencies = {}


def save_tasks(plan_id, tasks):
    try:
        __t.tasks[plan_id].update(tasks)
    except KeyError:
        __t.tasks[plan_id] = tasks


def save_dependencies(plan_id, dependencies):
    try:
        __t.dependencies[plan_id].update(dependencies)
    except KeyError:
        __t.dependencies[plan_id] = dependencies


def purge_all_tasks():
    __t.tasks = {}


def purge_all_dependencies():
    __t.dependencies = {}


def get_task_by_id(plan_id, task_id):
    try:
        tasks = __t.tasks[plan_id]
        return filter(lambda t: t.get_task_id() == task_id, tasks)[0]
    except KeyError:
        return None
    except IndexError:
        return None


def get_dependency(plan_id, _from, _to):
    try:
        dependencies = __t.dependencies[plan_id]
        return filter(lambda t: t.get_from() == _from and t.get_to() == _to, dependencies)[0]
    except KeyError:
        return None
    except IndexError:
        return None

def get_number_of_tasks():
    return len([item for sublist in __t.tasks.values() for item in sublist])


def get_number_of_dependencies():
    return len([item for sublist in __t.dependencies.values() for item in sublist])
