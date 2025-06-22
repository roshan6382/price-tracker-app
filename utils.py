# utils.py
import smtplib

def send_email(subject, body, to_email):
    from_email = "your_email@gmail.com"
    password = "your_gmail_app_password"  # App Password from Gmail settings

    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message)
