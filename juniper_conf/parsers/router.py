from niscanner.juniper_conf.parsers.base import ElementParser, get_hostname
from niscanner.juniper_conf.models import Router
from niscanner.juniper_conf.parsers.interfaces import InterfaceParser
from niscanner.juniper_conf.parsers.bgp import BgpPeeringParser


class RouterPaser:
    def parse(self, nodeTree, versionTree, physical_interfaces=[]):
        self._clean(nodeTree)
        doc = ElementParser(nodeTree)
        router = Router()
        router.name = get_hostname(doc)
        version_doc = ElementParser(versionTree)
        router.version = version_doc.first("junos-version").text()
        router.model = version_doc.first("product-model").text()
        router.interfaces = InterfaceParser().parse(nodeTree, physical_interfaces)
        router.bgp_peerings = BgpPeeringParser().parse(nodeTree)
        return router

    def _clean(self, nodeTree):
        # Remove unwanted stuff, e.g. logical-systems
        pass
