from kafka import KafkaProducer
from essential_generators import DocumentGenerator
import time

class KafkaEventProducer(object):
    _producer_instance = None

    def __init__(self, bootstrap_servers):

        self.bootstrap_servers = bootstrap_servers

        if KafkaEventProducer._producer_instance is None:

            kafka_configurations = {
                "value_serializer": lambda x: x.encode("utf-8"),
                "bootstrap_servers": self.bootstrap_servers,
                "api_version": (0, 10, 1),
            }

            KafkaEventProducer._producer_instance = KafkaProducer(
                **kafka_configurations
            )

    def send(self, topic, data) -> None:
        KafkaEventProducer._producer_instance.send(topic, data)
        KafkaEventProducer._producer_instance.flush()

def generate_word(word_generator: DocumentGenerator):
    word = word_generator.word()
    return word.lower()

if __name__ == "__main__":
    word_generator = DocumentGenerator()

    kafka_producer = KafkaEventProducer(["localhost:9092"])

    while True:
        word = generate_word(word_generator)
        print(f"Sending: {word}")
        kafka_producer.send("word-topic", generate_word(word_generator))
        print("Sent!")
        time.sleep(1)
