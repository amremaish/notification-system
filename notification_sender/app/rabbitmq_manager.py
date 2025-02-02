import pika
import time
import json
from app.config import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD


class RabbitMQManager:
    """Manages RabbitMQ connection and message operations."""

    def __init__(self):
        self.host = RABBITMQ_HOST
        self.credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(host=self.host, credentials=self.credentials)

    def connect_to_rabbitmq(self):
        """Retries RabbitMQ connection until it's available."""
        while True:
            try:
                connection = pika.BlockingConnection(self.parameters)
                print("✅ Connected to RabbitMQ")
                return connection
            except pika.exceptions.AMQPConnectionError:
                print("🚨 RabbitMQ not ready, retrying...")
                time.sleep(5)

    def send_notification(self, message_type: str, message_text: str):
        """Sends a JSON notification message to RabbitMQ."""
        connection = self.connect_to_rabbitmq()
        channel = connection.channel()

        # Declare queue to ensure it exists
        channel.queue_declare(queue="notifications", durable=True)

        message = json.dumps({"message_type": message_type, "message_text": message_text})

        channel.basic_publish(
            exchange="",
            routing_key="notifications",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
        )

        print(f"✅ Sent JSON Message: {message}")
        connection.close()


# ✅ Singleton instance for use in other modules
rabbitmq_manager = RabbitMQManager()
