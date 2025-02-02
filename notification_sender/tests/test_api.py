import pytest
from fastapi.testclient import TestClient

from app.rabbitmq_manager import rabbitmq_manager
from main import app

client = TestClient(app)

@pytest.fixture
def mock_rabbitmq(mocker):
    """Mock RabbitMQ to avoid actual message publishing."""
    mocker.patch.object(rabbitmq_manager, "send_notification", return_value=None)

def test_send_notification_chat(mock_rabbitmq):
    """Test sending a CHAT notification."""
    response = client.post("/send-notification/", json={"message_type": "CHAT", "message_text": "Hello, RabbitMQ!"})
    assert response.status_code == 200
    assert response.json() == {"status": "Message sent successfully"}

def test_send_notification_email(mock_rabbitmq):
    """Test sending an EMAIL notification."""
    response = client.post("/send-notification/", json={"message_type": "EMAIL", "message_text": "Test Email!"})
    assert response.status_code == 200
    assert response.json() == {"status": "Message sent successfully"}

def test_send_notification_invalid_type(mock_rabbitmq):
    """Test sending an invalid message type."""
    response = client.post("/send-notification/", json={"message_type": "INVALID", "message_text": "This should fail"})
    assert response.status_code == 422  # FastAPI auto-validates Pydantic schemas

def test_send_notification_missing_fields(mock_rabbitmq):
    """Test sending a message with missing fields."""
    response = client.post("/send-notification/", json={"message_type": "CHAT"})  # Missing `message_text`
    assert response.status_code == 422  # FastAPI auto-validates Pydantic schemas
