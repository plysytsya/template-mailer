![GitHub Actions status | sdras/awesome-actions](https://github.com/plysytsya/template-mailer/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/plysytsya/template-mailer/branch/master/graph/badge.svg)]

# template-mailer

A simple python client for sending mass emails from html templates.


## Description

The template-mailer lets you fill variables in html-templates and send the populated content via email.
It makes use of the jinja2 templating langauge ([Reference](https://jinja.palletsprojects.com/en/2.10.x/)).

## Usage

Provide your html-template as a string to the render_template-method:

    >>> from template_mailer import render_template
    >>> template = "<html> foo: {{ variable }} </html>"
    >>> data = {"variable": "bar"}
    >>> render_template(template, data)
    '<html> foo: bar </html>'


Use the SMTPClient to send the rendered template as html-email with the SMTPClient:


    >>> from template_mailer import SMTPClient
    >>> smtp_client = SMTPClient()
    >>> smtp_client.send("targetemailalldress@test.test", "subject", "message")

By default the client will look for the following environment variables:

`SMTP_HOST`,
`SMTP_PORT` (starttls),
`EMAIL_USER` (your email address),
`EMAIL_PASSWORD`

You can provide the SMTP configurations in plain form as well:

    >>> smtp_client = SMTPClient("smtp.gmail.com", 587, "your_email@gmail.coim", "your_password")


## Options

### Encryption
The default email encryption is TLS. An SSL option is not yet provided and will be part of a future release.

### Missing data
The render_template method will throw an error if you don't provide enough data to populate all template-variables:

    >>> from template_mailer import render_template
    >>> template = "<html> foo: {{ variable }} ham: {{ second_variable }} </html>"
    >>> data = {"variable": "bar"}
    >>> render_template(template, data)
    Traceback (most recent call last):
    ...
    jinja2.exceptions.UndefinedError: 'second_variable' is undefined

To change this policy you can provide the option undefined="allow" to the render_template-method:

    >>> from template_mailer import render_template
    >>> template = "<html> foo: {{ variable }} ham: {{ second_variable }} </html>"
    >>> data = {"variable": "bar"}
    >>> render_template(template, data, undefined="allow")
    '<html> foo: bar ham:  </html>'

### Logging
By default the SMTPClient uses the root-logger with log-level INFO. You can inject your own logger into the client:

    >>> from template_mailer import SMTPClient
    >>> import logging
    >>> some_logger = logging.getLogger("demo")
    >>> smtp_client = SMTPClient(logger=some_logger)

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
