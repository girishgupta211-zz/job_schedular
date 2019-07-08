import logging
import os
import socket
import uuid

from scheduler.apis import blueprint as scheduler_apiv1
from scheduler.app_settings import URL_PREFIX, APP_SECRET_KEY
from scheduler.config import config_by_name
from flask import Flask
from flask_cors import CORS
from flask_log_request_id import RequestID, RequestIDLogFilter, \
    current_request_id
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter


def register_blueprints(app):
    app.register_blueprint(scheduler_apiv1, url_prefix=URL_PREFIX)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class MachineInfoLogFilter(logging.Filter):
    def filter(self, log_record):
        log_record.machine_ip = socket.gethostname()
        log_record.env = os.getenv('FLASK_CONFIG') or 'dev'
        return log_record


def configure_logging(app):
    handler = logging.FileHandler(
        f'{app.config["LOGGING_DIR"]}/{app.config["LOGGING_FILE"]}')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(machine_ip)s %(env)s '
        '%(request_id)s %(name)s %(funcName)s:%(lineno)d %(message)s'))  # noqa
    handler.setLevel(getattr(logging, app.config["LOG_LEVEL"]))
    handler.addFilter(RequestIDLogFilter())
    handler.addFilter(MachineInfoLogFilter())
    app.logger.addHandler(handler)


def create_app():
    FLASK_CONFIG = os.getenv('FLASK_CONFIG') or 'dev'
    print(f'Loading {FLASK_CONFIG} configurations')

    app = Flask(__name__)
    RequestID(app,
              request_id_generator=lambda: f'scheduler_rid{uuid.uuid4().hex}')

    app.secret_key = APP_SECRET_KEY

    app.config.from_object(config_by_name[FLASK_CONFIG])

    postgres = {
        'user': app.config["POSTGRES_USER"],
        'pw': app.config["POSTGRES_PASSWORD"],
        'db': app.config["POSTGRES_DB"],
        'host': app.config["POSTGRES_HOST"],
        'port': app.config["POSTGRES_PORT"],
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres
    )

    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True

    app.url_map.converters['regex'] = RegexConverter

    # register blueprints
    register_blueprints(app)

    configure_logging(app)

    # enable cors
    CORS(app)

    return app


app = create_app()


@app.after_request
def append_request_id(response):
    response.headers.add('X-REQUEST-ID', current_request_id())
    return response


@app.route('/scheduler/health', methods=['GET'])
def health_check():
    return 'OK', 200
