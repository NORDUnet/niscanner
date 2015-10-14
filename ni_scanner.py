from ConfigParser import SafeConfigParser
from utils.cli import CLI
import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ni_scanner')

def main():
    args = CLI().options()
    try:
        config = SafeConfigParser()
        config.readfp(open(args.config))
    except IOError as (errno, strerror):
        logger.error("Config file '%s' is missing", args.config)

if __name__ == "__main__":
    main()
