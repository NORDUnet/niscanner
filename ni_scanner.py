from ConfigParser import SafeConfigParser
from utils.cli import CLI
from api.queue import Queue
from api.nerds import NerdsApi
from scanner.host import HostScanner
from scanner.exceptions import ScannerExeption
from utils.url import url_concat
import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ni_scanner')



def process_host(queue, nerds_api):
    item = queue.next("Host")
    while item:
        try: 
            queue.processing(item)
            scanner = HostScanner(item) 
            nerds = scanner.process()
            if not nerds:
                # Error occured :(
                logger.error("Unable to scan item "+str(item))
                queue.failed(item)
            else:
                logger.debug("Posting nerds data")
                nerds_api.send(nerds)
                queue.done(item)
        except ScannerExeption as e:
            logger.error("%s",e)
            failed(queue,item)
        except Exception as e:
            logger.error("Unable to process host %s got error: %s",item,str(e))
            failed(queue,item)
        item = queue.next("Host")

def failed(queue,item):
    try:
        queue.failed(item)
    except Exception as e:
        logger.error("Problem with reaching NI, got error: %s", e)


def main():
    args = CLI().options()
    try:
        config = SafeConfigParser()
        config.readfp(open(args.config))
    except IOError as (errno, strerror):
        logger.error("Config file '%s' is missing", args.config)
        return None
    ## ready :)
    api_user = config.get("NI", "api_user")
    api_key = config.get("NI", "api_key")
    queue_url = url_concat(config.get("NI", "url"), "scan_queue/")
    queue = Queue(queue_url, api_user, api_key)

    nerds_url = url_concat(config.get("NI", "url"), "nerds/")
    nerds_api = NerdsApi(nerds_url, api_user, api_key)
    
    process_host(queue, nerds_api)

if __name__ == "__main__":
    main()
