import logging, os


class EnvironmentConfig:
    """Base configuration"""

    TESTING = False

    BOOTSTRAP_SERVERS_STRING = os.getenv("BOOTSTRAP_SERVERS_STRING", "")
    BOOTSTRAP_SERVERS = BOOTSTRAP_SERVERS_STRING.split(",")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    KAFKA_LOG_LEVEL = os.getenv("KAFKA_LOG_LEVEL", "CRITICAL").upper()
    DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "") in (
        "True",
        "true",
        "TRUE",
        "",
        None,
    )
    logger_kafka = logging.getLogger("kafka")
    # TODO: Fing a way to handle loggers like <BrokerConnection node_id=bootstrap-0 host=b-2.b2b-dev-cluster.ji5eme.c6.kafka.us-east-2.amazonaws.com:9094 <connected> [IPv4 ('10.0.101.74', 9094)]>: socket disconnected
    # logger_kafka.addHandler(logging.StreamHandler(sys.stdout))
    logger_kafka.setLevel(KAFKA_LOG_LEVEL)
