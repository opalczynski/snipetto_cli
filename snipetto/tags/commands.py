import click

from snipetto.core.pagination import Paginator
from snipetto.tags.printer import Printer


@click.group()
@click.pass_context
def tags(ctx):
    """Tags entrypoint."""
    pass


@tags.command()
@click.pass_context
def list(ctx):
    """Will list all tags available in the system."""
    def tag_list(ctx, path=None):
        api = ctx.obj['api']
        response = api.request('tags', 'list', path=path)
        Printer(response).print()
        Paginator(response, ctx=ctx, method=tag_list).handle()
    tag_list(ctx)
