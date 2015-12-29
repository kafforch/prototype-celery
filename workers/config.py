from ConfigParser import ConfigParser


class WorkerConfigurator:
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
                BROKER_URL=self.__conf.get('Celery', 'broker'),
                CELERY_RESULT_BACKEND=self.__conf.get('Celery', 'backend'),
                CELERY_TASK_SERIALIZER='json',
                CELERY_ACCEPT_CONTENT=['json']
        )
