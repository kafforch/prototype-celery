from celery import Celery

app = Celery('celery_config', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', include=[
    'workers.plan_submitter',
])
