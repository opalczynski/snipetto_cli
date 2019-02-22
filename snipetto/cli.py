import click

from snipetto.core.services import APIService
from snipetto.snippets.commands import (
    add_snippet,
    delete_snippet,
    edit_snippet,
    get_snippet,
    list_snippet,
    search_snippet
)
from snipetto.tags.commands import tags


@click.group()
@click.pass_context
def entry_point(ctx):
    api_service = APIService()
    api_service.init()
    ctx.obj['api'] = api_service


entry_point.add_command(add_snippet)
entry_point.add_command(search_snippet)
entry_point.add_command(list_snippet)
entry_point.add_command(edit_snippet)
entry_point.add_command(tags)
entry_point.add_command(delete_snippet)
entry_point.add_command(get_snippet)


if __name__ == '__main__':
    entry_point(obj={})
