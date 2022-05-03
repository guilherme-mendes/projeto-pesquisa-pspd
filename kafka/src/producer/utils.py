from flask import current_app
from essential_generators import DocumentGenerator


class Generator:
    def __init__(self):
        self.word_generator = DocumentGenerator()

    def generate_word(self) -> str:
        return self.word_generator.word()


def generate_log_message(message, topic_name, quantity) -> str:
    logger_message = (
        f"{message}\n"
        f"Topic name: {topic_name}\n"
        f"Boostrap Servers: {current_app.config['BOOTSTRAP_SERVERS']}\n"
        f"Quantity: {quantity}"
    )
    return logger_message
