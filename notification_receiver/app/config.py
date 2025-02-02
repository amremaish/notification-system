import os

# MySQL Configurations
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql_db")
MYSQL_USER = os.getenv("MYSQL_USER", "admin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "admin")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "notifications")

# RabbitMQ Configurations
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")
