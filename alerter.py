import requests
import smtplib
from email.mime.text import MIMEText

SLACK_WEBHOOK = ''
EMAIL_ENABLED = False

def send_slack(message):
    if SLACK_WEBHOOK:
        try:
            requests.post(SLACK_WEBHOOK, json={'text': message})
            print("✅ Slack alert sent")
        except Exception as e:
            print(f"❌ Slack error: {e}")

def send_email(subject, body, to='admin@example.com'):
    if not EMAIL_ENABLED:
        return
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'your_email@gmail.com'
    password = 'your_app_password'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        print("✅ Email alert sent")
    except Exception as e:
        print(f"❌ Email error: {e}")