import json

from kafka import KafkaProducer


class KafkaEventProducer(object):
    _producer_instance = None

    def __init__(self, bootstrap_servers, development_mode=True):
        if type(bootstrap_servers) != list:
            raise ValueError(
                "The parameter boostrap_servers must be a list with at least one string element."
            )

        self.bootstrap_servers = bootstrap_servers

        if KafkaEventProducer._producer_instance is None:

            kafka_configurations = {
                "value_serializer": lambda python_dictionary: json.dumps(
                    python_dictionary
                ).encode("utf-8"),
                "key_serializer": lambda python_dictionary: json.dumps(
                    python_dictionary
                ).encode("utf-8"),
                "bootstrap_servers": self.bootstrap_servers,
                "api_version": (2, 8, 1),
                "acks": "all",
                "retries": 3,
            }

            if development_mode:
                KafkaEventProducer._producer_instance = KafkaProducer(
                    **kafka_configurations
                )
            else:
                KafkaEventProducer._producer_instance = KafkaProducer(
                    security_protocol="SSL",
                    **kafka_configurations,
                )

    def send(self, topic, event, key=None) -> None:
        KafkaEventProducer._producer_instance.send(topic, event, key)
        KafkaEventProducer._producer_instance.flush()
