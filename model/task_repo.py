# Dictionary, where:
#   key: plan_id
#   value: list of associated tasks
class Tasks:
    def __init__(self):
        pass


__t = Tasks()
__t.tasks = {}


def save(plan_id, tasks):
    try:
        __t.tasks[plan_id].update(tasks)
    except KeyError:
        __t.tasks[plan_id] = tasks


def purge_all_tasks():
    __t.tasks = {}


def get_by_id(plan_id, task_id):
    try:
        tasks = __t.tasks[plan_id]
        return filter(lambda t: t.get_task_id() == task_id, tasks)[0]
    except KeyError or IndexError:
        return None



def get_number_of_tasks():
    return len([item for sublist in __t.tasks.values() for item in sublist])
