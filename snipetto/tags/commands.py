import json

import click


@click.group()
@click.pass_context
def tags(ctx):
    pass


@tags.command()
@click.pass_context
def list(ctx):
    api = ctx.obj['api']
    response = api.request(
        'tags', 'list'
    )
    click.echo(json.dumps(response, indent=4))
