from fastapi import APIRouter
from app.schemas import Message
from app.rabbitmq_manager import rabbitmq_manager

router = APIRouter()

@router.post("/send-notification/")
def send_notification(message: Message):
    """API endpoint to send notifications via RabbitMQ."""
    rabbitmq_manager.send_notification(message.message_type, message.message_text)
    return {"status": "Message sent successfully"}
