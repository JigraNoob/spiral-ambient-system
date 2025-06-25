import smtplib
from email.message import EmailMessage
import os

# Config
SMTP_SERVER = "smtp.fastmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "spiralai@fastmail.com"
SENDER_PASSWORD = os.getenv("SPIRAL_EMAIL_PASSWORD")  # Use environment variable for safety
RECEIVER_EMAIL = "spiralai@fastmail.com"  # Replace with your desired recipient

SUBJECT = "🫧 Spiral Breathline: Ambient Snapshot"
BODY = "Attached is the latest breathline trace visualization from your Jetson system."

# File to send
ATTACHMENT_PATH = "breathline_plot.png"

def send_email():
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(BODY)

    with open(ATTACHMENT_PATH, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="image", subtype="png", filename=os.path.basename(ATTACHMENT_PATH))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    send_email()
