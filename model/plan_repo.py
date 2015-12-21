_plans = []


def save(plan):
    _plans.append(plan)


def get_by_id(id):
    try:
        return filter(lambda p: p.get_id() == id, _plans)[0]
    except IndexError:
        return None


def get_number_of_plans():
    return len(_plans)