import io
import random

from snipetto.cli import entry_point as cli
from tests.base import BaseSnippettoTestCase


class SnippetTestCase(BaseSnippettoTestCase):
    """Base test suite for snippetto CLI; it needs to be extended in the
    future. Currently tests assumes that you have snipetto_service available
    - which is not big deal, as this is dockerized."""

    @classmethod
    def setUpClass(cls):
        # add some snippet to be able to test something;
        super().setUpClass()
        cls.snippet_slug = 'randomname{}'.format(
            random.randint(0, 2000))  # nosec
        cls._create_snippet(cls.snippet_slug)

    @classmethod
    def _create_snippet(self, snippet_slug):
        result = self.runner.invoke(
            cli,
            args=[
                'add',
                '--slug', snippet_slug,
                '--tags', 'python,django',
                '--file', io.StringIO('import django'),
                '--desc', 'Test description'
            ],
            obj={}
        )
        return result

    def test_add(self):
        snippet_slug = 'randomnameadd{}'.format(
            random.randint(0, 2000))  # nosec
        result = self._create_snippet(snippet_slug)
        self.assertIn(snippet_slug, result.output)

    def test_delete(self):
        snippet_slug = 'randomnamedelete{}'.format(
            random.randint(0, 2000))  # nosec
        self._create_snippet(snippet_slug)
        result = self.runner.invoke(
            cli,
            args=[
                'delete', snippet_slug
            ],
            obj={}
        )
        confirm_string = 'Your snippet has been deleted.'
        self.assertIn(confirm_string, result.output)

    def test_edit(self):
        new_desc = 'Yet another new description.'
        result = self.runner.invoke(
            cli,
            args=[
                'edit', self.snippet_slug,
                '--desc', new_desc
            ],
            obj={}
        )
        self.assertIn(new_desc, result.output)

    def test_get(self):
        result = self.runner.invoke(
            cli,
            args=[
                'get', self.snippet_slug
            ],
            obj={}
        )
        self.assertIn(self.snippet_slug, result.output)

    def test_list(self):
        result = self.runner.invoke(
            cli,
            args=[
                'list',
            ],
            input='N',
            obj={}
        )
        self.assertIn(self.snippet_slug, result.output)

    def test_search(self):
        result = self.runner.invoke(
            cli,
            args=[
                'search',
                '--tags', 'python'
            ],
            input='N',
            obj={}
        )
        self.assertIn(self.snippet_slug, result.output)
