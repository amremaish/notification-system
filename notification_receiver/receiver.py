import pika
import time

# Retry mechanism to ensure RabbitMQ is up before connecting
def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ to start...")
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="notifications")

def callback(ch, method, properties, body):
    print(f"Received Notification: {body.decode()}")

channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)

print("Waiting for notifications...")
channel.start_consuming()
