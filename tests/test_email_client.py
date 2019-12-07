import unittest
import smtplib
from unittest.mock import MagicMock

from template_mailer.email_client import EmailClient


class TestEmailClient(unittest.TestCase):

    def setUp(self):
        self.email_client = EmailClient()
        smtplib.SMTP = MagicMock()

    def test_send(self):
        subject = "subject"
        html = "<p>test</p>"
        recipient = "testrecipient@test.test"
        self.email_client.send(subject, recipient, html)

    def test_connect(self):
        self.email_client.connect()


if __name__ == "__main__":
    unittest.main(verbosity=3)
