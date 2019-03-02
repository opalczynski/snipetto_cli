from click import ClickException


def get_snippet(start, end, file):
    if start and end:
        if start > end:
            raise ClickException('Start can not be bigger than end.')
        lines = file.readlines()[start:end]
        snippet = ''.join(lines)
    else:
        snippet = file.read()
    return snippet
