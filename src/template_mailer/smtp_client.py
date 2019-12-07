import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging

log_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)


class SMTPClient:
    def __init__(
        self,
        smtp_host=None,
        smtp_port=None,
        email_user=None,
        email_password=None,
        logger=logging.getLogger(),
    ):
        self.smtp_host = os.environ.get("SMTP_HOST", default=smtp_host)
        self.smtp_port = os.environ.get("SMTP_PORT", default=smtp_port)
        self.username = os.environ.get("EMAIL_USER", default=email_user)
        self.password = os.environ.get("EMAIL_PASSWORD", default=email_password)
        self.server = None
        self.logger = logger

    def send(self, recipient, subject, html):
        self.connect()
        message = self.build_message(subject, html)
        self.server.sendmail(self.username, recipient, message)
        self.logger.info("Sent email to %s" % recipient)
        self.server.quit()

    def connect(self):
        # Passing smtp-host two times to avoid python 3.7 bug.
        self.logger.info(
            "Connecting to %s with tls on port %s" % (self.smtp_host, self.smtp_port)
        )
        self.server = smtplib.SMTP(self.smtp_host)
        self.server.connect(self.smtp_host, self.smtp_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.username, self.password)
        self.logger.info("Established tls-connection with %s" % self.smtp_host)

    def disconnect(self):
        self.logger.info("Disconnecting from %s" % self.smtp_host)
        self.server.quit()
        self.logger.info("Disconnected from %s" % self.smtp_host)

    def build_message(self, subject, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        mime_text = MIMEText(html, "html")
        message.attach(mime_text)
        return message.as_string()
