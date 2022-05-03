import logging

from flask import Blueprint
from flask_api import FlaskAPI

from .config import EnvironmentConfig
from .core import core_router
from .kafkaconnect import KafkaEventProducer

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def create_app():
    app = FlaskAPI(__name__)

    app.config.from_object(EnvironmentConfig)
    app.register_blueprint(core_router, url_prefix="/api/v1")

    if EnvironmentConfig.BOOTSTRAP_SERVERS != [""]:
        development_mode = app.config["DEVELOPMENT_MODE"]
        KafkaEventProducer(
            bootstrap_servers=EnvironmentConfig.BOOTSTRAP_SERVERS,
            development_mode=development_mode,
        )
    else:
        logger.error(
            "Error connecting to kafka cluster. Bootstrap server misconfiguration."
        )

    return app
