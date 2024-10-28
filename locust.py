import uuid
from locust import HttpUser, task, between, events
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class AddToCartUser(HttpUser):
    wait_time = between(1, 5)
    token = 'jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiN2ZlMDBlYjUtN2JjNC00N2JmLWJkZTQtNWIwYTRlYWU1MTRkIiwiZXhwIjoxNzMwMTUxMjMwLCJ1c2VyX3R5cGUiOiJpbnRlcm5hbCIsInJvbGVzIjpbImFkbWluIl0sInNlc3Npb25fa2V5IjoiNGZmZjQ3ZWRmNGEzNGNhZmJmODllMGFkODdlZWRmMGUxMzM2MGYwNjQwZGIyMmFjYjNjOTg1YjgyMTE2Mjk0NiJ9.E5G76GenMQf-l7-Er4ArFUy-km3y5bXcCAbXWx6kVtY'
    host = "https://api.ecs.staging.biddano.com"

    @task
    def add_to_cart(self):
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json',
        }

        data = {
            "product_sku_id": "94b38d55-88eb-4d5c-89dc-1b6c9723c6ad",
            "mapped_bulk_buyer_id": "a2919a38-f407-404b-a847-2c8d6179988c",
            "quantity": 1
        }

        self.client.post(
            url="/api/v4/rust/orders/shortbuk/add_to_cart/",
            headers=headers,
            json=data
        )

    @task
    def cart_to_order(self):
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json',
        }

        data = {
            "mapped_bulk_buyer_id": "a2919a38-f407-404b-a847-2c8d6179988c",
            "order_by": "retailer",
            "request_id": str(uuid.uuid4())
        }

        self.client.post(
            url="/api/v4/orders/shortbuk/cart/cart_to_order/",
            headers=headers,
            json=data
        )


# Function to send the report via email after the Locust test ends
def send_email_with_report(report_path, recipient_email):
    sender_email = "vijaythoratvt00@gmail.com"
    sender_password = "czztmesocymlylcz"  # Use app-specific password if using Gmail 2FA
    subject = "Locust Test Report"
    body = "Please find the attached Locust test report."

    # Check if the report exists
    if not os.path.exists(report_path):
        print("Report file not found, unable to send email.")
        return

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the report file
    filename = os.path.basename(report_path)
    try:
        with open(report_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            msg.attach(part)

        # Set up the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print(f"Email sent to {recipient_email} with attachment {filename}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# This event hook runs when the Locust test stops
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    current_directory = os.getcwd()
    report_path = os.path.join(current_directory, "locust_report_stats.csv")
    recipient_email = "vijay.thorat@biddano.com"  # Update with the recipient email
    send_email_with_report(report_path, recipient_email)
