from workers.base_worker import app, repo


@app.task()
def store_plan(plan):
    plan_id = repo.plan_repo.save_new_plan(plan)
    repo.task_repo.save_new_tasks(plan_id, plan.get_tasks())
    repo.task_repo.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id
