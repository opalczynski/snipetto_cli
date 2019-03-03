

class TagParser:

    def __init__(self, raw_tags):
        self.raw_tags = raw_tags

    def parse(self):
        if self.raw_tags:
            return [
                {'name': tag.strip()} for tag in self.raw_tags.split(',')
            ]
        return None
