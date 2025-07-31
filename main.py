import smtplib
import os
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Read recipient emails
def get_recipients(file_path='recipients.txt'):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Attach files from attachments/ folder
def attach_files(msg, folder='attachments'):
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            ctype, encoding = mimetypes.guess_type(path)
            ctype = ctype or 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=filename)

# Send email
def send_email(subject, body, recipients):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(body)
    attach_files(msg)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent to {len(recipients)} recipients successfully.")
    except Exception as e:
        print(f"❌ Failed to send email. Error: {e}")

# Main Program
if __name__ == "__main__":
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email:\n")
    recipients = get_recipients()

    if not recipients:
        print("⚠️ No recipients found in recipients.txt")
    else:
        send_email(subject, body, recipients)
