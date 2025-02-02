from fastapi import FastAPI
from sender import send_notification

app = FastAPI()

@app.post("/send-notification/")
def send_notification_endpoint(notification: str):
    send_notification(notification)
    return {"status": "Notification sent"}
