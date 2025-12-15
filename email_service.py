import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    sender_email = "karan@gmail.com"
    sender_password = "abcd@A1"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("Email notification sent.")
    except Exception as e:
        print("Email failed:", e)

