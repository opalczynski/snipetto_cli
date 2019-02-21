import click

from snipetto.auth.commands import configure
from snipetto.snippets.commands import (
    add_snippet,
    delete_snippet,
    edit_snippet,
    get_snippet,
    search_snippet
)
from snipetto.tags.commands import tags


@click.group()
def entry_point():
    pass


entry_point.add_command(add_snippet)
entry_point.add_command(search_snippet)
entry_point.add_command(edit_snippet)
entry_point.add_command(tags)
entry_point.add_command(delete_snippet)
entry_point.add_command(get_snippet)
entry_point.add_command(configure)


if __name__ == '__main__':
    entry_point()
