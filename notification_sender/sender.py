import pika

def send_notification(notification: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications")
    channel.basic_publish(exchange="", routing_key="notifications", body=notification)
    connection.close()
