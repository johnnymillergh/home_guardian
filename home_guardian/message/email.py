import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from loguru import logger

from home_guardian.configuration.application_configuration import application_conf
from home_guardian.template.html_template import render_template

_mail_host: str = application_conf.get_string("email.mail_host")
_mail_username: str = application_conf.get_string("email.mail_username")
_mail_password: str = application_conf.get_string("email.mail_password")
_sender: str = (
    f"{_mail_username}{application_conf.get_string('email.mail_address_suffix')}"
)
_receivers: List[str] = application_conf.get_list("email.receivers")


def build_message(
    subject: str,
    receiver: str,
    template_name: str,
    render_dict: dict,
    picture_path: str,
) -> MIMEMultipart:
    """
    Builds a message with the given subject, receiver, template name and render dict.

    :param subject: The subject of the message.
    :param receiver: The receiver of the message.
    :param template_name: The name of the template to render.
    :param render_dict: The render dict for the template.
    :param picture_path: The path to the picture to attach.
    """
    content: MIMEText = MIMEText(
        render_template(template_name, render_dict),
        "html",
        "utf-8",
    )
    message: MIMEMultipart = MIMEMultipart("related")
    message["Subject"] = Header(subject, "utf-8").encode()
    message["From"] = Header(_sender)
    message["To"] = Header(receiver)
    message["Cc"] = Header(_sender)
    message.attach(content)
    file = open(picture_path, "rb")
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header("Content-ID", render_dict["content_id"])
    message.attach(img)
    return message


def send_email(
    subject: str, template_name: str, render_dict: dict, picture_path: str
) -> None:
    """
    Sends an email with the given subject, template name and render dict.

    :param subject: The subject of the message.
    :param template_name: The name of the template to render.
    :param render_dict: The render dict for the template.
    :param picture_path: The path to the picture to attach.
    """
    smtp: smtplib.SMTP = smtplib.SMTP(_mail_host, 25)
    smtp.connect(_mail_host, 25)
    smtp.login(_sender, _mail_password)
    for receiver in _receivers:
        message: MIMEMultipart = build_message(
            subject, receiver, template_name, render_dict, picture_path
        )
        logger.debug(f"Sending email. receiver: {receiver}")
        try:
            smtp.sendmail(_sender, [receiver], message.as_string())
            logger.debug(
                f"Sent email successfully. Receiver: {receiver}, subject: {subject}, template_name: {template_name}"
            )
        except smtplib.SMTPException:
            logger.exception("Exception occurred while sending email!")
    smtp.quit()
