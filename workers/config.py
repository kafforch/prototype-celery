from ConfigParser import ConfigParser


class WorkerConfigurator:
    def __init__(self, config_file="../../cfg/kafforch.cfg"):
        self.__conf = ConfigParser()
        self.__conf.readfp(open(config_file))

    def get_simple_redis_url(self):
        return self.__conf.get("Redis", "simple_url")

    def get_celery_config_kwargs(self):
        return dict(
                broker=self.__conf.get('Celery', 'broker'),
                backend=self.__conf.get('Celery', 'backend')
        )
