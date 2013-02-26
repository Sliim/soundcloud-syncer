import sys
import unittest
from mock import Mock
from mock import MagicMock

sys.path.insert(0, "../../")
from ssyncer.suser import suser
from ssyncer.strack import strack

def mock_get_likes_failure(uri):
    return False

def mock_get_likes_success(uri):
    def json_res():
        return b'[{"kind":"track","id":1337,"title":"Foo","permalink":"foo","user":{"permalink":"user1"}},{"kind":"track","id":1338,"title":"Bar","permalink":"bar","user":{"permalink":"user2"}},{"kind":"track","id":1339,"title":"Baz","permalink":"baz","user":{"permalink":"user3"}}]'

    response = MagicMock()
    response.read = json_res
    return response

class TestSuser(unittest.TestCase):

    def test_object_require_client(self):
        """ Test object initialization raise exception if client missing. """
        self.assertRaises(Exception, suser.__init__, "Foo")

    def test_object_has_good_name(self):
        """ Test object has name `foo`. """
        client = Mock()
        object = suser("Foo", client=client)
        self.assertEqual("Foo", object.name)

    def test_get_likes_on_failure(self):
        """ Test get user's likes when an error occured. """
        client = MagicMock()
        client.get = mock_get_likes_failure
        object = suser("Foo", client=client)

        self.assertFalse(object.get_likes())

    def test_get_likes_on_success(self):
        """ Test get user's likes when success. """
        client = MagicMock()
        client.get = mock_get_likes_success
        object = suser("Foo", client=client)

        likes = object.get_likes()
        self.assertEquals(3, len(likes))
        for like in likes:
            self.assertIsInstance(like, strack)
