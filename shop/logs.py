from logging.handlers import RotatingFileHandler
import logging
from flask import current_app

def info():
    handler = RotatingFileHandler('log.log', maxBytes=10240, backupCount=2)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    handler.setLevel(logging.INFO)
    current_app.logger.addHandler(handler)

    current_app.logger.setLevel(logging.INFO)
    current_app.logger.info('Shop startup')

info()

