# Dictionary, where:
#   key: plan_id
#   value: list of associated tasks
class Tasks:
    def __init__(self):
        pass


__t = Tasks()
__t.tasks = {}


def save(plan_id, task):
    try:
        __t.tasks[plan_id].append(task)
    except KeyError:
        __t.tasks[plan_id] = [task]


def purge_all_tasks():
    __t.tasks = {}


def get_by_id(plan_id, task_id):
    try:
        return filter(lambda t: task_id == t.get_task_id(), __t.tasks[plan_id])[0]
    except KeyError:
        return None


def get_number_of_tasks():
    return len([item for sublist in __t.tasks.values() for item in sublist])
