from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os

load_dotenv("./.env")
GMAIL = os.environ.get("GMAIL")
PASSWORD = os.environ.get("GMAIL_PASSWORD")


def send_email(message):

    subject = "Posts this week from the /r/Calgary careers discussion thread."
    message = message

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = GMAIL
    msg['From'] = GMAIL

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # specify location of the email providers smtp
        connection.starttls()  # a way to secure connection to our email server by encrypting message
        connection.ehlo()  # initiates SMTP communication using an EHLO (Extended Hello) command instead of the HELO command - additional SMTP commands are often available
        connection.login(user=GMAIL, password=PASSWORD)  # log in by providing a username and password
        # connection.sendmail(from_addr=FROM_EMAIL,
        #                     to_addrs=to_email,
        #                     msg=f"Subject:{subject}\n\n{message}")
        connection.send_message(msg)    # use for HTML enabled messages
