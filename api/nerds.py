from urllib.parse import urljoin
from api.http.request import PostRequest
import json
import urllib.request, urllib.error, urllib.parse

class NerdsApi:
    def __init__(self, url, user, api_key):
        self.url = url
        self.api_auth = "ApiKey {}:{}".format(user,api_key)

    def send(self, data):
        if not isinstance(data, str):
            data = json.dumps(data)
        req = PostRequest(self.url, data)
        req.header("Authorization", self.api_auth)
        req.post()

