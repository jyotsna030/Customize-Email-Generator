import smtplib
from email.mime.text import MIMEText

def send_email_smtp(recipient, subject, body, smtp_server, smtp_port, email, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
