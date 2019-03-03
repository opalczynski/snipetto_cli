from datetime import datetime

import click


class Printer:
    """We would like to have snippets very nicely printed in the output."""

    def __init__(self, json_snippet, is_list=False):
        if not is_list:
            self.json_snippet = [json_snippet]
        else:
            self.json_snippet = json_snippet['results']

    def _format_time(self, time_str):
        return datetime.strptime(
            time_str, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime(
            "%H:%M:%S - %d, %b %Y"
        )

    def print_message(self, message=None):
        if message:
            click.echo(message)

    def print(self, message=None, snippet_only=False, skip_snippet=False):
        if snippet_only:
            for json_data in self.json_snippet:
                self.print_snippet(json_data, snippet_only=snippet_only)
            return
        self.print_message(message=message)
        for json_data in self.json_snippet:
            self.print_header(json_data)
            if not skip_snippet:
                self.print_snippet(json_data)
            self.print_separator()

    def print_header(self, json_data):
        """
        Make this small - vertical space matters.
        Basic information goes here:
            * slug
            * created at
            * updated at
            * author
        """
        click.echo("Snippet slug (ID {}, author {}): {}".format(
            json_data['id'],
            json_data['author']['username'],
            click.style(json_data['slug'], bold=True, fg='blue'),
        ))
        click.echo("Created: {}\tUpdated: {}".format(
            self._format_time(json_data['created_at']),
            self._format_time(json_data['updated_at'])
        ))
        click.echo("Tags: {}".format(
            click.style(
                ', '.join(tag['name'] for tag in json_data['tags']),
                bold=True, fg='green'
            )
        ))
        if json_data['description']:
            click.echo("Description: {}".format(
                json_data['description']
            ))

    def print_snippet(self, json_data, snippet_only=False):
        if snippet_only:
            click.echo(json_data['snippet'])
        else:
            click.echo('Snippet:')
            click.echo()
            click.echo(json_data['snippet'])

    def print_separator(self):
        click.echo(79*'-')
