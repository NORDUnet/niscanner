from configparser import ConfigParser
from utils.cli import CLI
from api.queue import Queue
from api.nerds import NerdsApi
from scanner.host import HostScanner
from scanner.router import RouterScanner
from scanner.exceptions import ScannerExeption
from utils.url import url_concat
import json
import sys
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
                logger.error("Unable to scan item %s", str(item))
                queue.failed(item)
            else:
                logger.debug("Posting nerds data")
                nerds_api.send(nerds)
                queue.done(item)
        except ScannerExeption as e:
            logger.error("%s", e)
            failed(queue, item)
        except Exception as e:
            logger.error("Unable to process host %s got error: %s", item, str(e))
            failed(queue, item)
        item = queue.next("Host")


def failed(queue, item):
    try:
        queue.failed(item)
    except Exception as e:
        logger.error("Problem with reaching NI, got error: %s", e)


def process_router(queue, nerds_api, username, password):
    item = queue.next("Router")
    while item:
        try:
            queue.processing(item)
            scanner = RouterScanner(item, username, password)
            nerds = scanner.process()
            if not nerds:
                logger.error("Unable to scan router %s", str(item))
                queue.failed(item)
            else:
                logger.debug("Posting nerds data")
                nerds_api.send(nerds)
                queue.done(item)
        except Exception as e:
            logger.error("Unable to process router %s got error: %s", item, str(e))
            failed(queue, item)
        item = queue.next("Router")


def main():
    args = CLI().options()

    try:
        config = ConfigParser()
        config.read(args.config)
    except IOError:
        logger.error("Config file '%s' is missing", args.config)
        return None
    
    if args.target:
        # Local scan mode, to circumvent the need for an NI instance and queue.
        # Just scan the specified target and print the NERDS JSON to stdout.
        username = config.get("ssh", "user")
        password = config.get("ssh", "password")
        item = {"data": args.target}
        scanner = RouterScanner(item, username, password)
        nerds = scanner.process()
        if not nerds:
            logger.error("Unable to scan %s", args.target)
            sys.exit(1)
        print(json.dumps(nerds, indent=4, sort_keys=True))
        return
    
    # ready :)
    api_user = config.get("NI", "api_user")
    api_key = config.get("NI", "api_key")
    queue_url = url_concat(config.get("NI", "url"), "scan_queue/")
    queue = Queue(queue_url, api_user, api_key)

    nerds_url = url_concat(config.get("NI", "url"), "nerds/")
    nerds_api = NerdsApi(nerds_url, api_user, api_key)

    process_host(queue, nerds_api)

    if config.has_section("ssh"):
        router_user = config.get("ssh", "user")
        router_pass = config.get("ssh", "password")
        process_router(queue, nerds_api, router_user, router_pass)


if __name__ == "__main__":
    main()
