import click
from click import ClickException
from snipetto.core.services import ActionTypeE
from snipetto.snippets.parsers import TagParser
from snipetto.snippets.printer import Printer


@click.command(name='get')
@click.argument('slug', type=str)
@click.option('--snippet-only', 'snippet_only', is_flag=True,
              type=bool, required=False)
@click.pass_context
def get_snippet(ctx, slug, snippet_only):
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
@click.option('--slug', 'slug', type=str, required=True)
@click.option('--tags', 'tags', type=str, required=True)
# for now auto adding just from the file
@click.option('--file', 'file', type=click.File('r'), required=True)
@click.option('--start', 'start', type=int, required=False)
@click.option('--end', 'end', type=int, required=False)
@click.pass_context
def add_snippet(ctx, slug, tags, file, start, end):
    api = ctx.obj['api']
    tags = TagParser(raw_tags=tags).parse()

    if start and end:
        if start > end:
            raise ClickException('Start can not be bigger than end.')
        lines = file.readlines()[start:end]
        snippet = ''.join(lines)
    else:
        snippet = file.read()

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
@click.option('--tags', 'tags', type=str)
# for now auto adding just from the file
@click.option('--file', 'file', type=click.File('r'))
@click.pass_context
def edit_snippet(ctx, slug, tags, file):
    api = ctx.obj['api']
    instance_id = api.get_id_by_slug(slug)
    tags = TagParser(raw_tags=tags).parse()
    if not file and not tags:
        raise ClickException("Sorry, nothing to edit.")
    json_data = {}
    for option in [
        ('snippet', file.read() if file else None),
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
@click.option('--tags', 'tags', type=str)
# for now auto adding just from the file
@click.option('--slug', 'slug', type=str)
@click.pass_context
def search_snippet(ctx, slug, tags):
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
    api = ctx.obj['api']
    response = api.request(
        'snippets', 'list'
    )
    Printer(json_snippet=response, is_list=True).print()
