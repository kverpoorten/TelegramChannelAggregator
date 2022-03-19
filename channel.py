class Channel:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def test_filter(self, message):
        return self.regex.match(message) != None
