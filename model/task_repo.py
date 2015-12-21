_tasks = []


def save(task):
    _tasks.append(task)


def purge_all_tasks():
    del _tasks [:]


def get_by_id(plan_id, task_id):
    try:
        return filter(lambda t: plan_id == t.get_plan_id() and task_id == t.get_task_id(), _tasks)[0]
    except IndexError:
        return None


def get_number_of_tasks():
    return len(_tasks)
