import pytest
from unittest.mock import MagicMock
from app.consumer import process_message
from app.database import db_manager


@pytest.fixture
def mock_db_manager(mocker):
    """Mock the database manager to avoid actual DB operations."""
    mocker.patch.object(db_manager, "insert_message", return_value=None)


def test_process_message_chat(mock_db_manager):
    """Test processing a CHAT message."""
    channel = MagicMock()  # Mock RabbitMQ channel
    method = MagicMock()   # Mock RabbitMQ delivery method
    properties = MagicMock()  # Mock RabbitMQ properties

    # Use a valid JSON message
    body = b'{"message_type": "CHAT", "message_text": "Hello, this is a chat message"}'

    # Call the function to test
    process_message(channel, method, properties, body)

    # Check database insert was called correctly
    db_manager.insert_message.assert_called_once_with("CHAT", "Hello, this is a chat message")

    # Check message acknowledgment
    channel.basic_ack.assert_called_once_with(delivery_tag=method.delivery_tag)


def test_process_message_email(mock_db_manager):
    """Test processing an EMAIL message."""
    channel = MagicMock()  # Mock RabbitMQ channel
    method = MagicMock()   # Mock RabbitMQ delivery method
    properties = MagicMock()  # Mock RabbitMQ properties

    # Use a valid JSON message
    body = b'{"message_type": "EMAIL", "message_text": "This is an email message"}'

    # Call the function to test
    process_message(channel, method, properties, body)

    # Check database insert was called correctly
    db_manager.insert_message.assert_called_once_with("EMAIL", "This is an email message")

    # Check message acknowledgment
    channel.basic_ack.assert_called_once_with(delivery_tag=method.delivery_tag)
