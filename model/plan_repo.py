_plans = []


def save(plan):
    _plans.append(plan)


def purge_all_plans():
    del _plans [:]


def get_plan_by_id(plan_id):
    try:
        return filter(lambda p: plan_id == p.get_plan_id(), _plans)[0]
    except IndexError:
        return None


def get_number_of_plans():
    return len(_plans)
