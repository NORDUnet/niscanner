import argparse

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description="NI scan on demand")
        parser.add_argument("-C", "--config", default="settings.conf")

        local = parser.add_argument_group("local scan mode (no NI instance required)")
        local.add_argument(
            "--target",
            metavar="HOST",
            default=None,
            help="Scan this target directly and print NERDS JSON to stdout "
                 "instead of polling the NI queue.",
        )
        local.add_argument(
            "--type",
            metavar="TYPE",
            default="Router",
            help="Queue item type for local mode (default: Router).",
        )

        self.parser = parser

    def options(self):
        return self.parser.parse_args()
