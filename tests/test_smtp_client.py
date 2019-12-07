import unittest
import smtplib
from unittest.mock import MagicMock

from template_mailer import SMTPClient


class TestSMTPClient(unittest.TestCase):

    def setUp(self):
        self.smtp_client = SMTPClient()
        smtplib.SMTP = MagicMock()

    def test_send(self):
        subject = "subject"
        html = "<p>test</p>"
        recipient = "testrecipient@test.test"
        self.smtp_client.send(subject, recipient, html)

    def test_connect(self):
        self.smtp_client.connect()


if __name__ == "__main__":
    unittest.main(verbosity=3)
