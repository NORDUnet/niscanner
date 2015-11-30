from scanner.exceptions import ScannerExeption
import nmap
import json
import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('host_scanner')

try:
    from lib.nmap_services_py import nerds_format, merge_nmap_services
except ImportError as e:
    logger.error("No nerds_format and merge_nmap_services to import. Check if you have a symlink to 'lib/nmap_services_py.py'")

class HostScanner:
    # -O requires root access and is slow 
    nmap_arguments = "-PE -sV -O --osscan-guess"
    #nmap_arguments = "-PE -sV"

    def __init__(self, item):
        data = item["data"]
        try:
            data = json.loads(data)
            self.target = data["target"]
            self.ipv4s = data.get("ipv4s", [])
        except ValueError:
            # no nestest structure. Target is data
            self.target = data
            self.ipv4s = []

    def process(self):
        nm = nmap.PortScanner()
        to_scan = self.ipv4s or [self.target]
        nerds = None
        for target in to_scan:
            result = nm.scan(target, arguments=self.nmap_arguments) 
            if result["scan"]:
                scan_data = result["scan"]
                for ip in sorted(scan_data.keys()):
                    if nerds:
                        #merge the data
                        new_nerds = nerds_format(ip, result)
                        nerds = merge_nmap_services(new_nerds, nerds) 
                    else:
                        nerds = nerds_format(ip, result)
            else:
                # TODO: Better/prettier error handling
                if "nmap" in result: 
                    if "error" in result["nmap"]["scaninfo"]:
                        errors = result["nmap"]["scaninfo"]["error"]
                        msg = "Unable to scan target '{}' error '{}'".format(self.target, errors)
                        logger.warning(msg)
                    elif "downhosts" in result["nmap"]["scanstats"]:
                        if result["nmap"]["scanstats"]["downhosts"] > 0:
                            msg = "Host '{}' was not reachable".format(self.target) 
                            logger.warning(msg)
        return nerds
        

