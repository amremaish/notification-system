import pika
import time


def connect_to_rabbitmq():
    """Retries RabbitMQ connection until it's available."""
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(host="rabbitmq", credentials=credentials)

    retries = 10  # Max retries
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(parameters)
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"🚨 RabbitMQ not ready, retrying... ({i + 1}/{retries})")
            time.sleep(5)  # Wait before retrying

    raise Exception("Failed to connect to RabbitMQ after multiple attempts.")


def send_notification(notification: str):
    """Sends a notification message to RabbitMQ."""
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    # ✅ Ensure queue is declared with the same settings as in receiver.py
    channel.queue_declare(queue="notifications", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=notification,
        properties=pika.BasicProperties(delivery_mode=2)  # ✅ Make messages persistent
    )
    print(f"✅ Sent Notification: {notification}")
    connection.close()
