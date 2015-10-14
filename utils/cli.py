import argparse

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description="NI scan on demand")
        parser.add_argument("-C", "--config", default="settings.conf")

        self.parser = parser

    def options(self):
        return self.parser.parse_args()
