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

    def get_celery_config_kwargs(self):
        return dict(
                broker=self.__conf.get('Celery', 'broker'),
                backend=self.__conf.get('Celery', 'backend')
        )
