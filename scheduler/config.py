import os
from pathlib import Path

from dotenv import load_dotenv

SCHEDULER_ENV_PATH = os.getenv('SCHEDULER_ENV_PATH', '.')
if SCHEDULER_ENV_PATH:
    env_path = Path(SCHEDULER_ENV_PATH) / '.env'
    print(f"Loading config from {env_path}")
    load_dotenv(dotenv_path=env_path, verbose=True, override=True)
else:
    print(f"`SCHEDULER_ENV_PATH` not specified. Loading defaults")


class Config(object):
    DEBUG = False
    TESTING = False
    ENV = os.getenv('FLASK_CONFIG', 'dev')

    LOGGING_DIR = os.getenv('LOGGING_DIR', '/tmp/')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOGGING_FILE = os.getenv('LOGGING_FILE', 'app.log')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class QAConfig(Config):
    DEBUG = True
    TESTING = True


class LoadConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    qa=QAConfig,
    load=LoadConfig,
    preprod=LoadConfig,
    prod=ProductionConfig
)
