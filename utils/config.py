from ConfigParser import ConfigParser


class KafforchConfigurator:
    def __init__(self, config_file="../../cfg/kafforch.cfg"):
        self.__conf = ConfigParser()
        self.__conf.readfp(open(config_file))

    def get_redis_config_kwargs(self):
        return dict(
                host=self.__conf.get("DEFAULT", "Redis.host"),
                port=self.__conf.get("DEFAULT", "Redis.port"),
                db=self.__conf.get("DEFAULT", "Redis.db")
        )

    def get_celery_config_dict(self):
        return dict(
                BROKER_URL=self.__conf.get('Celery-Connection', 'broker'),
                CELERY_RESULT_BACKEND=self.__conf.get('Celery-Connection', 'backend'),
                CELERY_TASK_SERIALIZER=self.__conf.get('Celery-Connection', 'serializer'),
                CELERY_ACCEPT_CONTENT=[self.__conf.get('Celery-Connection', 'serializer')],
                CELERY_IMPORTS=self.__conf.get('Celery-Connection', 'imports').split(',')
        )

    def get_plan_starter_cycle_time(self):
        return int(self.__conf.get("Plan-Starter", "cycle_time_secs"))

    def get_task_starter_cycle_time(self):
        return int(self.__conf.get("Task-Starter", "cycle_time_secs"))

    def get_value(self, section, key):
        return self.__conf.get(section, key)