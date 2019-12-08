import unittest
import smtplib
import warnings

from template_mailer import SMTPClient


class SMTPStub:
    def __init__(
        self, host="", port=0, local_hostname=None, timeout=10, source_address=None
    ):
        self.host = host
        self.port = port
        self.status = self.init_status()
        self.tls_status = 0
        self.status_codes = {
            250: (250, b"2.0.0 OK n5sm550235eda.15 - gsmtp"),
            235: (235, b"2.7.0 Accepted"),
            220: (220, b"2.0.0 Ready to start TLS"),
            221: (221, b"2.0.0 closing connection c20sm579884edt.67 - gsmtp"),
        }

    def init_status(self):
        if self.host != "":
            return 250
        else:
            return 0

    def connect(self, host, port):
        self.status = 220

    def ehlo(self):
        pass

    def login(self, user, password):
        if self.tls_status in [220, 235]:
            self.tls_status = 235
            self.status = 250
        else:
            raise smtplib.SMTPNotSupportedError

    def sendmail(self, from_addr, to_addrs, msg, mail_options=(), rcpt_options=()):
        if "@" not in from_addr or "@" not in to_addrs:
            raise smtplib.SMTPRecipientsRefused
        else:
            return {}

    def starttls(self):
        self.tls_status = 220

    def quit(self):
        self.status = 0

    def noop(self):
        if self.status != 0:
            return self.status_codes[self.status]
        else:
            raise smtplib.SMTPServerDisconnected


class TestSMTPClient(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=ResourceWarning, message="unclosed.*"
        )
        username = "testuser@test.com"
        password = "supersecretpassword"
        smtp_host = "test.testhost.com"
        smtp_port = 587
        self.smtp_client = SMTPClient(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            email_user=username,
            email_password=password,
        )
        smtplib.SMTP = SMTPStub
        self.smtp_client.connect()

    def test_send(self):
        self.smtp_client.connect()
        subject = "subject"
        html = "<p>test</p>"
        self.smtp_client.send(
            recipient=self.smtp_client.username, subject=subject, html=html
        )

    def test_connect(self):
        self.smtp_client.connect()
        status = self.smtp_client.server.noop()
        status_code = status[0]
        self.assertEqual(status_code, 250)

    def test_disconnect(self):
        error = False
        self.smtp_client.disconnect()
        try:
            self.smtp_client.server.noop()
        except smtplib.SMTPServerDisconnected:
            error = True
        self.assertTrue(error)

    def test_build_message(self):
        subject = "mock subject"
        message = "hello, world!"
        mime = self.smtp_client.build_message(subject, message)
        self.assertIn("Content-Type: multipart/alternative;", mime)


if __name__ == "__main__":
    unittest.main(verbosity=3)
