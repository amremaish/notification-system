# Notification System

## Overview
This project is a microservices-based **Notification System** that allows sending and receiving notifications using **FastAPI**, **RabbitMQ**, and **MySQL**. It consists of two main services:
- **Notification Sender**: Exposes an API to send notifications.
- **Notification Receiver**: Listens for notifications and stores them in a database.

## Architecture
The system follows a **producer-consumer** architecture using RabbitMQ:
1. The **sender** service receives a notification request via a FastAPI endpoint.
2. The **sender** publishes the message to a RabbitMQ queue.
3. The **receiver** listens for messages and processes them.
4. The **receiver** saves messages to the MySQL database.

## Technologies Used
- **FastAPI** (Backend API)
- **RabbitMQ** (Message Broker)
- **MySQL** (Database)
- **Docker & Docker Compose** (Containerization)
- **Pytest** (Testing Framework)

## Project Structure
```
notification-system/
├── notification_sender/
│   ├── app/
│   │   ├── api.py
│   │   ├── main.py
│   │   ├── rabbitmq_manager.py
│   │   ├── schemas.py
│   │   ├── database.py
│   ├── tests/
│   │   ├── test_api.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── notification_receiver/
│   ├── app/
│   │   ├── consumer.py
│   │   ├── database.py
│   │   ├── rabbitmq_manager.py
│   ├── tests/
│   │   ├── test_consumer.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── docker-compose.yml
├── README.md
```

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/notification-system.git
cd notification-system
```

### **2. Build and Run the Services**
```bash
docker-compose up --build
```
This starts:
- **RabbitMQ** (Message Broker)
- **MySQL** (Database)
- **Notification Sender** (FastAPI API for sending notifications)
- **Notification Receiver** (Consumes messages from RabbitMQ)

### **3. Sending a Notification**
Use **Postman** or `curl` to send a request:
```bash
curl -X POST "http://localhost:8000/send-notification/" \
     -H "Content-Type: application/json" \
     -d '{"message_type": "CHAT", "message_text": "Hello, RabbitMQ!"}'
```

### **4. Running Tests**
To run tests, use:
```bash
docker-compose run notification_sender_tests
```
```bash
docker-compose run notification_receiver_tests
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/send-notification/` | Send a new notification |

## Environment Variables
These variables are used inside `docker-compose.yml`:
```env
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=notifications
MYSQL_USER=admin
MYSQL_PASSWORD=admin
```

## Notes
- The **test services** are excluded when running `docker-compose up --build`. To run tests, use `docker-compose --profile test up`.
- The database schema includes a `messages` table with columns: `id`, `message_type`, `message_text`, and `is_received`.
- The RabbitMQ Management UI is accessible at **http://localhost:15672** (username: `admin`, password: `admin`).