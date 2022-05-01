from flask import current_app

def generate_log_message(message, topic_name, event):
    logger_message = (
        f"{message}\n"
        f"Topic name: {topic_name}\n"
        f"Boostrap Servers: {current_app.config['BOOTSTRAP_SERVERS']}\n"
        f"event: {event}"
    )
    return logger_message