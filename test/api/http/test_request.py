from api.http.request import BaseRequest, PutRequest, GetRequest
import unittest

class BaseRequestTest(unittest.TestCase):

    def setUp(self):
        self.req = BaseRequest("http://example.com/")

    def test_set_data_with_content_type(self):
        self.req.data('{"test":"data"}', "application/json")
        self.assertEqual(self.req.headers["Content-Type"], "application/json") 
        self.assertEqual(self.req._data, '{"test":"data"}')

    def test_set_data_no_content_type(self):
        self.req.data('{"test":"data"}')
        self.assertEqual(self.req.headers, {}) 
        self.assertEqual(self.req._data, '{"test":"data"}')

    def test_set_data_converts_to_post(self):
        self.req.data('{"test":"data"}', "application/json")
        real = self.req._request()
        self.assertEqual(real.get_data(), '{"test":"data"}')
        self.assertEqual(real.get_method(), "POST")
    
    def test_query_parms(self):
        self.req.query("status","test").query("type", "test")
        self.assertEqual(self.req.query_params["status"], "test")
        self.assertEqual(self.req.query_params["type"], "test")
        real = self.req._request()
        self.assertEqual(real.get_full_url(), "http://example.com/?status=test&type=test")

    def test_header(self):
        self.req.header("X-Auth-Token", "sweet-test").header("X-Test", "test")
        self.assertEqual(len(self.req.headers), 2)
        self.assertEqual(self.req.headers["X-Auth-Token"], "sweet-test")
        self.assertEqual(self.req.headers["X-Test"], "test")
        real = self.req._request()
        # headers are capital - lowercase in urllib2
        self.assertEqual(real.get_header("X-test"), "test")
        self.assertTrue(real.get_header("X-auth-token"), "sweet-test")

    def test_content_type(self):
        self.req.content_type("application/xml")
        self.assertEqual(self.req.headers["Content-Type"], "application/xml")


class PutRequestTest(unittest.TestCase):

    def test_put_request(self):
        req = PutRequest("http://example.com/")
        req.data('{"test":"best"}', "application/json")
        real = req._request()
        self.assertEqual(real.get_data(), '{"test":"best"}')
        self.assertEqual(real.get_method(), "PUT")

class GetRequestTest(unittest.TestCase):

    def test_get_request(self):
        req = GetRequest("http://example.com/")
        req.header("Test", "test")
        real = req._request()
        self.assertEqual(real.get_method(),"GET")
        self.assertEqual(real.get_header("Test"),"test")
