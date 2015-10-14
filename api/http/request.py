import urllib2
from urllib import urlencode

class BaseRequest(object):
    
    def __init__(self, url):
        self.url = url
        self.query_params = {}
        self.headers = {}
        self._data=None

    def query(self, name, value):
        self.query_params[name] = value
        return self

    def header(self,field, value):
        self.headers[field] = value
        return self

    def content_type(self, value):
       self.header("Content-Type", value) 
       return self
    
    def data(self, req_data, content_type=None):
        if content_type:
            self.content_type(content_type)
        self._data = req_data
        return self

    def _execute(self):
        return urllib2.urlopen(self._request())

    def _request(self):
        url = self.url
        if self.query_params:
            url = "{0}?{1}".format(self.url, urlencode(self.query_params))
        #Create req
        req = urllib2.Request(url)
        
        for field, value in self.headers.iteritems():
            req.add_header(field, value)
        if self._data:
            req.add_data(self._data)
        return req   
           

    def open(self):
        return self._execute()

class GetRequest(BaseRequest):
    pass

class PutRequest(BaseRequest):
    def _request(self):
        req = BaseRequest._request(self)
        req.get_method = lambda: "PUT"
        return req

    def put(self):
        self._execute()
