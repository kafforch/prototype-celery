import plan_repo_simple, plan_repo_redis


def factory(_intype):
    if _intype == "TEST":
        return plan_repo_simple
    if _intype == "REDIS":
        return plan_repo_redis