#!/usr/bin/env python
# coding: utf-8

# In[31]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class EmailClient:
    def __init__(self, SMTP_HOST=None, SMTP_PORT=None, EMAIL_USER=None, EMAIL_PASSWORD=None):
        self.smtp = os.environ.get("SMTP_HOST", default=SMTP_HOST)
        self.port = os.environ.get("SMTP_PORT", default=SMTP_PORT)
        self.username = os.environ.get("EMAIL_USER", default=EMAIL_USER)
        self.password = os.environ.get("EMAIL_PASSWORD", default=EMAIL_PASSWORD)

    def send(self, subject, recipient, html):
        self.connect()
        message = self.build_message(html)
        self.server.sendmail(self.username, recipient, message)
        self.server.quit()

    def connect(self):
        # Passing smtp-host two times to avoid python 3.7 bug.
        self.server = smtplib.SMTP(self.smtp)
        self.server.connect(self.smtp, self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.username, self.password)

    def build_message(self, html):
        message = MIMEMultipart('alternative')
        mime_text = MIMEText(html, 'html')
        message.attach(mime_text)
        return message.as_string()
