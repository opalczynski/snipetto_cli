import click
from click import ClickException
from snipetto.core.services import ActionTypeE
from snipetto.snippets.parsers import TagParser
from snipetto.snippets.printer import Printer
from snipetto.snippets.helpers import get_snippet


@click.command(name='get')
@click.argument('slug', type=str)
@click.option('--snippet-only', 'snippet_only', is_flag=True,
              type=bool, required=False,
              help='Will return content of the snippet only.')
@click.pass_context
def get_snippet(ctx, slug, snippet_only):
    """Will return snippet details by slug.

    You can user here --snippet-only flag and redirect the stream
    directly to file."""
    api = ctx.obj['api']
    instance_id = api.get_id_by_slug(slug)
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.GET,
        id=instance_id,
    )
    Printer(json_snippet=response).print(snippet_only=snippet_only)


@click.command(name='delete')
@click.argument('slug', type=str)
@click.pass_context
def delete_snippet(ctx, slug):
    """Will delete the snippet from your base."""
    api = ctx.obj['api']
    instance_id = api.get_id_by_slug(slug)
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.DELETE,
        id=instance_id,
    )
    Printer(json_snippet=response).print_message(
        message='Your snippet has been deleted.'
    )


@click.command(name='add')
@click.option('--slug', 'slug', type=str, required=True,
              help="The snippet slug.")
@click.option('--tags', 'tags', type=str, required=True,
              help="The snippet tags, comma separated list.")
@click.option('--file', 'file', type=click.File('r'), required=True,
              help="The file from which snippet will be created.")
@click.option('--start', 'start', type=int, required=False,
              help="Start line number in file. Optional.")
@click.option('--end', 'end', type=int, required=False,
              help="End line number in file. Optional.")
@click.pass_context
def add_snippet(ctx, slug, tags, file, start, end):
    """Allows to add new snippet to your base.

    Current implementation allows to add snippets from files -
    it is possible to specify start and end lines to pick only
    interesting content from file. If tag is not existing - it will
    be created."""
    api = ctx.obj['api']
    tags = TagParser(raw_tags=tags).parse()
    snippet = get_snippet(start, end, file)

    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.CREATE,
        json={
            "snippet": snippet,
            "tags": tags,
            "slug": slug
        }
    )
    Printer(json_snippet=response).print(
        message='Your snippet has been added.'
    )


@click.command(name='edit')
@click.argument('slug', type=str)
@click.option('--tags', 'tags', type=str,
              help="The snippet tags, comma separated list.")
# for now auto adding just from the file
@click.option('--file', 'file', type=click.File('r'),
              help="The file from which snippet will be created.")
@click.option('--start', 'start', type=int, required=False,
              help="Start line number in file. Optional.")
@click.option('--end', 'end', type=int, required=False,
              help="End line number in file. Optional.")
@click.pass_context
def edit_snippet(ctx, slug, tags, file, start, end):
    """Will edit snippet with given slug.

    It allows to override tags and file. You can also specify start and end
    lines numbers."""
    api = ctx.obj['api']
    instance_id = api.get_id_by_slug(slug)
    tags = TagParser(raw_tags=tags).parse()
    if not file and not tags:
        raise ClickException("Sorry, nothing to edit.")
    json_data = {}
    for option in [
        ('snippet', get_snippet(start, end, file) if file else None),
        ('tags', tags),
        ('slug', slug)
    ]:
        if option[1]:
            json_data.update({option[0]: option[1]})

    edit_response = api.request(
        'snippets', 'list',
        action=ActionTypeE.EDIT,
        id=instance_id,
        json=json_data
    )
    Printer(json_snippet=edit_response).print(
        message='Your snippet has been edited.'
    )


@click.command(name='search')
@click.option('--tags', 'tags', type=str,
              help="The snippet tags, comma separated list.")
# for now auto adding just from the file
@click.option('--slug', 'slug', type=str,
              help="The snippet slug - unique identifier. Search is of type"
                   " startswith - so multiple results can be returned.")
@click.pass_context
def search_snippet(ctx, slug, tags):
    """Allows to search for snippets.

    Search is based on tag and slug. Tags search is AND
    like - this means that if you specify two tags: `python,django` only
    those snippets will be returned that have both tags.
    """
    if not tags and not slug:
        raise ClickException("One of the option needs "
                             "to be provided: slug, tags, or both.")
    api = ctx.obj['api']
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.LIST,
        params={
            "tags": tags,
            "slug": slug
        }
    )
    Printer(json_snippet=response, is_list=True).print()


@click.command(name='list')
@click.pass_context
def list_snippet(ctx):
    """Will list snippets available in your base."""
    api = ctx.obj['api']
    response = api.request(
        'snippets', 'list'
    )
    Printer(json_snippet=response, is_list=True).print()
