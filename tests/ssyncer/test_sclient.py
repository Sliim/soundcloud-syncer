import sys
import unittest

sys.path.insert(0, "../../")
from ssyncer.sclient import sclient

class TestSclient(unittest.TestCase):

    def test_init(self):
        """ Test basic object initialization. """
        object = sclient("my_id")
        self.assertEquals("my_id", object.client_id)

    def test_init_with_kwargs(self):
        """ Test object initialization with kwargs. """
        object = sclient("my_id", host="my_host", port="my_port")
        self.assertEquals("my_host", object.host)
        self.assertEquals("my_port", object.port)

    def test_get_protocol_https(self):
        """ Test get protocol when port equals 443. """
        object = sclient("my_id", port="443")
        self.assertEquals("https", object.get_protocol())

    def test_get_protocol_http(self):
        """ Test get protocol when port is different to 443. """
        object = sclient("my_id", port="80")
        self.assertEquals("http", object.get_protocol())
