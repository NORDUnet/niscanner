import json
import logging
import sys

logger = logging.getLogger('router_scanner')

try:
    from juniper_conf.juniper_conf import scan_remote_host
except ImportError as e:
    logger.error(
        "Could not import juniper_conf. "
        "Check that niscanner/juniper_conf is a symlink to "
        "nerds/producers/juniper_conf."
    )
    logger.error('Import error: %s', e)
    sys.exit(1)


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
