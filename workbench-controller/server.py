import logging

from flask import Flask
from flask_cors import CORS
from restapi import bp
from h1st_saas import config

app = Flask(__name__)
CORS(app)

app.register_blueprint(bp, url_prefix=config.RESTAPI_URL_PREFIX)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    logger = logging.getLogger('h1st_saas')
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
