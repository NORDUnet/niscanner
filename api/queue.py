from urlparse import urljoin
from api.http.request import GetRequest, PutRequest
import json
import urllib2

class Queue:

    def __init__(self, url):
        self.url = url


    def next(self,itemType):
        result = None
        try: 
            req = GetRequest(self.url)
            req.query("status", "QUEUED").query("type", itemType)
            req.header('Authorization', 'ApiKey markus:7e7bb84b6d08f8401fb3df47511d2473a2b396d7')
            resp = req.open()
            obj = json.load(resp)
            if len(obj["objects"]) > 0:
                item = obj["objects"][0]
                item["status"] = "PROCESSING"
                put_url = urljoin(self.url,item["resource_uri"])

                req2 = PutRequest(put_url)
                req2.data(json.dumps(item), "application/json")
                req2.header('Authorization', 'ApiKey markus:7e7bb84b6d08f8401fb3df47511d2473a2b396d7')
                req2.put()
                result = item
        except urllib2.HTTPError, e:
            #Got an error
            None
        return result


