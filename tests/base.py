from unittest import TestCase

from click.testing import CliRunner

from snipetto.cli import entry_point as cli


class BaseSnippettoTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.test_username = 'opalczynski'
        cls.test_password = 'pass1234'
        # invoke runner once to create credentials file:
        cls.runner.invoke(
            cli,
            args=['tags', 'list'],
            input='{}\n{}\nN\n'.format(cls.test_username, cls.test_password),
            obj={}
        )
