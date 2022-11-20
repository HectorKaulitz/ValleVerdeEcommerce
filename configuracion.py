class BaseConfig:
    DEBUG = True
    SECRET_KEY = "algo"
    TESTING = True

class DevConfig(BaseConfig):
    pass

class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False