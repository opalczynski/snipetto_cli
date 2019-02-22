import json

import click
from click import ClickException
from snipetto.core.services import ActionTypeE


@click.command(name='get')
@click.argument('slug', type=str)
@click.pass_context
def get_snippet(ctx, slug):
    api = ctx.obj['api']
    # TODO: make some helper for that too.
    # make search by slug to find id first
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.LIST,
        params={
            "slug": slug
        }
    )
    if len(response["results"]) != 1:
        raise ClickException("More (or None) snippets found. "
                             "Check out your slug.")
    instance_id = response["results"][0]["id"]
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.GET,
        id=instance_id,
    )
    click.echo(json.dumps(response, indent=4))


@click.command(name='delete')
@click.argument('slug', type=str)
@click.pass_context
def delete_snippet(ctx, slug):
    api = ctx.obj['api']
    # TODO: make some helper for that too.
    # make search by slug to find id first
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.LIST,
        params={
            "slug": slug
        }
    )
    if len(response["results"]) != 1:
        raise ClickException("More (or None) snippets found. "
                             "Check out your slug.")
    instance_id = response["results"][0]["id"]
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.DELETE,
        id=instance_id,
    )
    click.echo(json.dumps(response, indent=4))


@click.command(name='add')
@click.option('--slug', 'slug', type=str, required=True)
@click.option('--tags', 'tags', type=str, required=True)
# for now auto adding just from the file
@click.option('--file', 'file', type=click.File('r'), required=True)
@click.pass_context
def add_snippet(ctx, slug, tags, file):
    api = ctx.obj['api']
    tags_list = []
    for tag in tags.split(','):
        tags_list.append({'name': tag})
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.CREATE,
        json={
            "snippet": file.read(),
            "tags": tags_list,
            "slug": slug
        }
    )
    click.echo(json.dumps(response, indent=4))


@click.command(name='edit')
@click.argument('slug', type=str)
@click.option('--tags', 'tags', type=str)
# for now auto adding just from the file
@click.option('--file', 'file', type=click.File('r'))
@click.pass_context
def edit_snippet(ctx, slug, tags, file):
    api = ctx.obj['api']
    # TODO: make some helper for that too.
    # make search by slug to find id first
    response = api.request(
        'snippets', 'list',
        action=ActionTypeE.LIST,
        params={
            "slug": slug
        }
    )
    if len(response["results"]) != 1:
        raise ClickException("More (or None) snippets found. "
                             "Check out your slug.")
    instance_id = response["results"][0]["id"]
    # TODO: make some helper for that
    tags_list = []

    if tags is not None:
        for tag in tags.split(','):
            tags_list.append({'name': tag})
    if not file and not tags:
        raise ClickException("Sorry, nothing to edit.")
    json_data = {}
    for option in [
        ('snippet', file.read() if file else None),
        ('tags', tags_list),
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
    click.echo(json.dumps(edit_response, indent=4))


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
    click.echo(json.dumps(response, indent=4))


@click.command(name='list')
@click.pass_context
def list_snippet(ctx):
    api = ctx.obj['api']
    response = api.request(
        'snippets', 'list'
    )
    click.echo(json.dumps(response, indent=4))
