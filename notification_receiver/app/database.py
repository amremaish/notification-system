import mysql.connector
import time
from app.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

class DatabaseManager:
    """Handles all database operations."""
    def __init__(self):
        self.db = self.connect_to_mysql()
        self.create_messages_table()

    def connect_to_mysql(self):
        """Connect to MySQL with retry logic."""
        while True:
            try:
                connection = mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DATABASE
                )
                print("✅ Connected to MySQL")
                return connection
            except mysql.connector.Error:
                print("🚨 MySQL not ready, retrying...")
                time.sleep(5)

    def create_messages_table(self):
        """Creates the messages table if it doesn't exist."""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message_type ENUM('CHAT', 'EMAIL') NOT NULL,
                message_text TEXT NOT NULL
            )
        """)
        self.db.commit()
        print("✅ Messages table is ready.")

    def insert_message(self, message_type, message_text):
        """Inserts a new message into the database."""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO messages (message_type, message_text) VALUES (%s, %s)",
            (message_type, message_text),
        )
        self.db.commit()
        print(f"📩 Stored Message: {message_text} as {message_type}")

# Singleton instance of DatabaseManager
db_manager = DatabaseManager()
