import unittest
from jinja2.exceptions import UndefinedError
from template_mailer import render_template


class TestMailMerge(unittest.TestCase):

    def test_render_template(self):
        template = "hello, {{ somevar }}"
        data = {"somevar": "world!"}
        rendered = render_template(template, data)
        self.assertEqual(rendered, "hello, world!")

    def test_undefined(self):
        template = "No spam: {{ spam }} {{ eggs }}"
        data = {"eggs": "easter"}
        error = False
        try:
            render_template(template, data)
        except UndefinedError:
            error = True
        self.assertTrue(error)


if __name__ == "__main__":
    unittest.main(verbosity=3)
