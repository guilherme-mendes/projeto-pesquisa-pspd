import logging, os, sys

from flask import Blueprint, current_app, request
from flask_api import status

from .kafkaconnect import KafkaEventProducer

from .utils import generate_log_message

core_router = Blueprint("core", __name__)

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


@core_router.route("/internal-events/", methods=["POST"])
def register_internal_event():
    logger.debug("REGISTERING INTERNAL EVENT")
    resultant_data = request.data

    topic_name = resultant_data["topic"]
    key = resultant_data["key"]
    event_data = resultant_data["event"]

    logger_message = generate_log_message(
        "Posting internal event in kafka.", topic_name, resultant_data["event"]
    )

    logger.debug(logger_message)

    try:
        producer = KafkaEventProducer(
            bootstrap_servers=current_app.config["BOOTSTRAP_SERVERS"],
            development_mode=current_app.config["DEVELOPMENT_MODE"],
        )
        result = producer.send(topic_name, event_data, key)
    except Exception as exc:
        logger.error(
            "An error occurred while posting internal event.",
            exc_info=True,
            extra={
                "request": request,
                "data": resultant_data,
                "topic_name": topic_name,
            },
        )
        return {
            "message": "Error posting internal event in kafka.",
        }, status.HTTP_400_BAD_REQUEST
    else:
        return result, status.HTTP_201_CREATED


@core_router.route("/status/", methods=["GET"])
def healthcheck():
    return {"status": "healthy"}, status.HTTP_201_CREATED
