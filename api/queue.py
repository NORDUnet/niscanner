from urlparse import urljoin
from api.http.request import GetRequest, PutRequest
import json
import urllib2

class Queue:

    def __init__(self, url, user, api_key):
        self.url = url
        self.api_auth = "ApiKey {}:{}".format(user,api_key)


    def next(self,itemType):
        result = None
        try: 
            req = GetRequest(self.url)
            req.query("status", "QUEUED").query("type", itemType)
            req.header('Authorization', self.api_auth)
            resp = req.open()
            obj = json.load(resp)
            if len(obj["objects"]) > 0:
                result = obj["objects"][0]
        except urllib2.HTTPError:
            #Got an error
            None
        return result

    def failed(self,item):
        try:
            item["status"] = "FAILED"
            self._put(item)
        except urllib2.HTTPError as e:
            # Got an error putting
            None

    def processing(self, item):
        try:
            item["status"] = "PROCESSING"
            self._put(item)
        except urllib2.HTTPError as e:
            None

    def done(self, item):
        try:
            item["status"] = "DONE"
            self._put(item)
        except urllib2.HTTPError as e:
            # Got an error putting
            None


    def _put(self,item):
        put_url = urljoin(self.url, item["resource_uri"])
        req = PutRequest(put_url)
        req.data(json.dumps(item), "application/json")
        req.header("Authorization", self.api_auth)
        req.put()

