import click


class Paginator:

    def __init__(self, response, ctx, method):
        self.response = response
        self.ctx = ctx
        self.method = method

    def has_next(self):
        return 'next' in self.response and self.response['next'] is not None

    def get_next(self):
        return self.response['next']

    def handle(self):
        if self.has_next():
            if click.confirm('Do you want to see next page?'):
                self.method(self.ctx, path=self.get_next())
