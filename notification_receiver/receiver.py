import pika
import time

def connect_to_rabbitmq():
    """Retries RabbitMQ connection until it's available."""
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(host="rabbitmq", credentials=credentials)

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            print("✅ Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("🚨 RabbitMQ not ready, retrying...")
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="notifications", durable=True)
def callback(ch, method, properties, body):
    """Prints received notifications."""
    print(f"📩 Received Notification: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=False)
channel.start_consuming()
