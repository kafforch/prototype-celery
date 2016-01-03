class Consts:
    pass

const = Consts()

const.PLAN_ID_SEED = "global_plan_id"

const.PLAN_PREFIX = "plan-"
const.TASKS_PREFIX = "tasksof-"
const.DEPENDENCIES_PREFIX = "dependenciesof-"

const.PLAN_KEY = const.PLAN_PREFIX + "{}"
const.TASKS_OF_PLAN = const.TASKS_PREFIX + "{}"
const.DEPENDENCIES_OF_PLAN = const.DEPENDENCIES_PREFIX + "{}"

const.PLAN_WILDCARD = const.PLAN_PREFIX + "*"
const.TASKS_WILDCARD = const.TASKS_PREFIX + "*"
const.DEPENDENCIES_WILDCARD = const.DEPENDENCIES_PREFIX + "*"
