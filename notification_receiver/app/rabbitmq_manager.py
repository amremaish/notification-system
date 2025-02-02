import pika
import time
from app.config import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD

class RabbitMQManager:
    """Manages RabbitMQ connection and message consumption."""

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

    def start_consumer(self, callback):
        """Starts consuming messages from RabbitMQ."""
        connection = self.connect_to_rabbitmq()
        channel = connection.channel()

        # Declare queue to ensure it exists
        channel.queue_declare(queue="notifications", durable=True)

        print("✅ Waiting for notifications... Press Ctrl+C to exit.")
        channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=False)

        channel.start_consuming()


# ✅ Singleton instance for use in other modules
rabbitmq_manager = RabbitMQManager()
