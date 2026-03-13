import json
import logging

logger = logging.getLogger('router_scanner')

from niscanner.juniper_conf.juniper_conf import scan_remote_host



class RouterScanner:
    def __init__(self, item, username, password):
        data = item["data"]
        try:
            data = json.loads(data)
            self.target = data["target"]
        except (ValueError, KeyError):
            self.target = data
        self.username = username
        self.password = password

    def process(self):
        router = scan_remote_host(self.target, self.username, self.password)
        if not router:
            logger.error("Failed to fetch configuration from %s", self.target)
            return None
        return {
            'host': {
                'name': router.name.lower(),
                'version': 1,
                'juniper_conf': router.to_json(),
            }
        }
