from snipetto.cli import entry_point as cli
from tests.base import BaseSnippettoTestCase


class TagTestCase(BaseSnippettoTestCase):

    def test_tag_list(self):
        result = self.runner.invoke(
            cli,
            args=['tags', 'list'],
            obj={}
        )
        self.assertIn('Tags', result.output)
