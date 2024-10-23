import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import os

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Use these variables in your email configuration


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)  # Login to the email account
            server.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASSWORD
    recipient_email = "vijay.thorat@biddano.com"
    subject = "Test Email for terrafom"
    body = "This is a test email sent from Python."

    send_email(sender_email, sender_password, recipient_email, subject, body)
