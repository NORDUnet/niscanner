from ConfigParser import SafeConfigParser
from utils.cli import CLI
from api.queue import Queue
from scanner.host import HostScanner
from utils.url import url_concat
import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ni_scanner')

try:
    from lib.nmap_services_py import nerds_format
except ImportError as e:
    logger.error("No nerds_format to import. Check if you have a symlink to 'lib/nmap_services_py.py'")


def process_host(queue):
    item = queue.next("Host")
    if item:
        scanner = HostScanner(item, nerds_format) 
        nerds = scanner.process()
        if not nerds:
            # Error occured :(
            logger.error("Unable to scan item "+str(item))
            queue.failed(item)
        else:
            print nerds
            queue.done(item)
        


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
    
    process_host(queue)

if __name__ == "__main__":
    main()
