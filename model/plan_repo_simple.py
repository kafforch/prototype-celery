import uuid


class Plans:
    def __init__(self):
        pass


__p = Plans()
__p.plans = []


def get_id():
    plan_id = str(uuid.uuid4())

    while get_plan_by_id(plan_id) is not None:
        plan_id = str(uuid.uuid4())

    return plan_id


def save(plan):
    plan_id = plan.get_plan_id()
    if plan_id is None:
        plan_id = get_id()
        plan.set_plan_id(plan_id)

    __p.plans.append(plan)

    return plan_id


def purge_all_plans():
    del __p.plans[:]


def get_plan_by_id(plan_id):
    try:
        return filter(lambda p: plan_id == p.get_plan_id(), __p.plans)[0]
    except IndexError:
        return None


def get_number_of_plans():
    return len(__p.plans)
