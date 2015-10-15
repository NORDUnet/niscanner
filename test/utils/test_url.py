from utils.url import url_concat
import unittest

class UrlConcatTest(unittest.TestCase):

    def test_slash_on_base_and_chunk(self):
        result = url_concat("https://nordu.net/test/","/some/path")
        self.assertEqual(result, "https://nordu.net/test/some/path")

    def test_no_slashses(self):
        result = url_concat("https://nordu.net/test","some/path")
        self.assertEqual(result, "https://nordu.net/test/some/path")

    def test_only_base(self):
        result = url_concat("https://nordu.net/test/","some/path")
        self.assertEqual(result, "https://nordu.net/test/some/path")

    def test_only_chunk(self):
        result = url_concat("https://nordu.net/test","/some/path")
        self.assertEqual(result, "https://nordu.net/test/some/path")
