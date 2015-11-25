from scanner.exceptions import ScannerExeption
import nmap
import json

class HostScanner:
    # -O requires root access and is slow 
    #nmap_arguments = "-PE -sV -O --osscan-guess"
    nmap_arguments = "-PE -sV"

    def __init__(self, item, nmap_format):
        data = item["data"]
        try:
            data = json.loads(data)
            self.target = data["target"]
        except ValueError:
            # no nestest structure. Target is data
            self.target = data
        self.nmap_format = nmap_format

    def process(self):
        nm = nmap.PortScanner()
        result = nm.scan(self.target, arguments=self.nmap_arguments) 
        if result["scan"]:
            scan_data = result["scan"]
            for ip in sorted(scan_data.keys()):
                nerds = self.nmap_format(ip, result)
            return nerds
        else:
            # TODO: Better/prettier error handling
            if "nmap" in result: 
                if "error" in result["nmap"]["scaninfo"]:
                    errors = result["nmap"]["scaninfo"]["error"]
                    msg = "Unable to scan target '{}' error '{}'".format(self.target, errors)
                    raise ScannerExeption(msg)
                elif "downhosts" in result["nmap"]["scanstats"]:
                    if result["nmap"]["scanstats"]["downhosts"] > 0:
                        msg = "Host '{}' was not reachable".format(self.target) 
                        raise ScannerExeption(msg)
            return None

        

