import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CARRIER = os.getenv("CARRIER")

HOST = "smtp.gmail.com"
PORT_NUMBER = 587

SMS_CARRIERS = {
    "AT&T": "@txt.att.net",
    "Sprint": "@messaging.sprintpcs.com",
    "T-Mobile": "@tmomail.net",
    "Verizon": "@vtext.com",
    "Metro PCS": "@mymetropcs.com",
}


def send_email(new_vehicles):
    msg_sms = create_message(new_vehicles, PHONE_NUMBER, CARRIER)
    msg_email = create_message(new_vehicles, EMAIL_ADDRESS, None)
    with smtplib.SMTP(HOST, PORT_NUMBER) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg_sms)
        smtp.send_message(msg_email)
        smtp.close()


def create_message(new_vehicles, recipient, carrier) -> EmailMessage:

    msg = EmailMessage()
    msg["To"] = (
        EMAIL_ADDRESS if carrier is None else f"{recipient}{SMS_CARRIERS[CARRIER]}"
    )
    msg["From"] = EMAIL_ADDRESS
    msg["Subject"] = "New Parts for DC Integra!"
    msg.set_content(format_content(new_vehicles))

    return msg


def format_content(new_vehicles):
    msg_content = ""
    
    return msg_content