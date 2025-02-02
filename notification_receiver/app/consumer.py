from app.rabbitmq_manager import rabbitmq_manager
from app.database import db_manager
import json

def process_message(ch, method, properties, body):
    """Handles incoming JSON messages and stores them in MySQL."""
    try:
        # ✅ Decode JSON message
        message_data = json.loads(body.decode())

        message_type = message_data.get("message_type", "CHAT")
        message_text = message_data.get("message_text", "")

        # Validate message type
        if message_type not in ["CHAT", "EMAIL"]:
            print(f"🚨 Invalid message type: {message_type}")
            return

        # Store message in the database
        db_manager.insert_message(message_type, message_text)
        print(f"📩 Stored JSON Message: {message_text} as {message_type}")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        print("🚨 Invalid JSON format received!")

def start_consumer():
    """Starts the RabbitMQ consumer using RabbitMQManager."""
    rabbitmq_manager.start_consumer(process_message)
