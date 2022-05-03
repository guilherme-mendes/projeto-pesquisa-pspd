import logging, os, sys

from flask import Blueprint, current_app, request
from flask_api import status

from .kafkaconnect import KafkaEventProducer

from .utils import generate_log_message, Generator

core_router = Blueprint("core", __name__)

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

TOPIC_NAME = "word-topic"


@core_router.route("/word-flow/", methods=["POST"])
def register_internal_event():
    logger.debug("Request received")
    resultant_data = request.data

    word_qtt = resultant_data["word_qtt"]

    logger_message = generate_log_message(
        "Posting words in event in kafka.", TOPIC_NAME, word_qtt
    )

    logger.debug(logger_message)

    try:
        producer = KafkaEventProducer(
            bootstrap_servers=current_app.config["BOOTSTRAP_SERVERS"],
            development_mode=current_app.config["DEVELOPMENT_MODE"],
        )
        generator = Generator()
        for _ in range(word_qtt):
            word = generator.generate_word()
            producer.send(TOPIC_NAME, word)
    except Exception as exc:
        logger.error(
            f"An error occurred while posting words in kafka topic. Error: {exc}"
        )
        return {
            "message": "Error posting words in kafka topic.",
        }, status.HTTP_400_BAD_REQUEST
    else:
        return {"status": "ok"}, status.HTTP_201_CREATED


@core_router.route("/status/", methods=["GET"])
def healthcheck():
    return {"status": "healthy"}, status.HTTP_200_OK
