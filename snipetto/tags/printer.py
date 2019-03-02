import click


class Printer:

    def __init__(self, json_tags):
        self.tags = json_tags['results']
        self.count = json_tags['count']

    def print(self):
        click.echo()
        click.echo("Tags (currently {} in the system): ".format(
            self.count
        ))
        for tag in self.tags:
            click.echo('\t * {}'.format(tag['name']))
