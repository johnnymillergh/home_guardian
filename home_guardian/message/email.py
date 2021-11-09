import datetime
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from loguru import logger

from home_guardian.configuration.application_configuration import application_conf

mail_host: str = application_conf.get_string("email.mail_host")
mail_user: str = application_conf.get_string("email.mail_user")
mail_password: str = application_conf.get_string("email.mail_password")
sender: str = f"{mail_user}{application_conf.get_string('email.mail_address_suffix')}"
receivers: List[str] = application_conf.get_list("email.receivers")


def build_message(receiver: str) -> MIMEMultipart:
    content: MIMEText = MIMEText(
        "This is a email from Python "
        + datetime.datetime.now().strftime("%Y-%m-%d %T"),
        "plain",
        "utf-8",
    )
    message: MIMEMultipart = MIMEMultipart()
    message["Subject"] = Header(
        "Emergency Security Alert, at "
        + datetime.datetime.now().strftime("%Y-%m-%d %T"),
        "utf-8",
    )
    message["From"] = Header(sender)
    message["To"] = Header(receiver)
    message["Cc"] = Header(sender)
    message.attach(content)
    return message


def send_email() -> None:
    smtp: smtplib.SMTP = smtplib.SMTP(mail_host, 25)
    smtp.connect(mail_host, 25)
    smtp.login(sender, mail_password)
    for receiver in receivers:
        message: MIMEMultipart = build_message(receiver)
        try:
            logger.info(f"Sending email. receiver: {receiver}")
            smtp.sendmail(sender, [receiver], message.as_string())
            logger.info(
                f"Sent email successfully. {smtp}. receiver: {receiver}, message: {message}"
            )
        except smtplib.SMTPException:
            logger.exception("Exception occurred while sending email!")
    smtp.quit()
