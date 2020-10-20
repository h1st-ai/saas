import logging

from flask import Flask
import sys
from flask_cors import CORS
from restapi import bp
from h1st_saas import config

app = Flask(__name__)


if config.RESTAPI_CORS_ORIGIN:
    origins = [s.strip() for s in config.RESTAPI_CORS_ORIGIN.split(",")]
    CORS(app, origins=origins)

app.register_blueprint(bp, url_prefix=config.RESTAPI_URL_PREFIX)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logger = logging.getLogger('h1st_saas')

    if gunicorn_logger.handlers:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

        logger.handlers = gunicorn_logger.handlers
        logger.setLevel(gunicorn_logger.level)
        logger.propagate = True
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
