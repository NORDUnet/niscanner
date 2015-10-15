from ConfigParser import SafeConfigParser
from utils.cli import CLI
from api.queue import Queue
from utils.url import url_concat
import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ni_scanner')

def process_host(queue):
    item = queue.next("Host")
    if item:
        None
        None
        


def main():
    args = CLI().options()
    try:
        config = SafeConfigParser()
        config.readfp(open(args.config))
    except IOError as (errno, strerror):
        logger.error("Config file '%s' is missing", args.config)
        return None
    ## ready :)
    queue_url = url_concat(config.get("NI", "url"), "scan_queue")
    queue = Queue(queue_url, config.get("NI","api_user"), config.get("NI","api_key"))

if __name__ == "__main__":
    main()
