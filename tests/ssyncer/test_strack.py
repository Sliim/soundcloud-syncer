import sys
import os
import json
import unittest
from mock import Mock

sys.path.insert(0, "../../")
from ssyncer.strack import strack

json_data = json.loads('[{"kind":"track","id":1337,"title":"Foo","permalink":"foo","user":{"permalink":"user1"}},{"kind":"track","id":1338,"title":"Bar","permalink":"bar","user":{"permalink":"user2"}},{"kind":"track","id":1339,"title":"Baz","permalink":"baz","user":{"permalink":"user3"}}]')

class TestStrack(unittest.TestCase):

    def setUp(self):
        """ This testsuite create temporary dir/files. Delete them before tests. """
        if os.path.exists("/tmp/user1/1337-foo.mp3"):
            os.remove("/tmp/user1/1337-foo.mp3")
        if os.path.exists("/tmp/user1"):
            os.rmdir("/tmp/user1")

    def test_metadata(self):
        """
        Test metadata has been loaded from json object
        and get method return metadata value from a given key.
        """
        client = Mock()

        object = strack(json_data[0], client=client)
        self.assertEquals(1337, object.get("id"))
        self.assertEquals("Foo", object.get("title"))
        self.assertEquals("foo", object.get("permalink"))
        self.assertEquals("user1", object.get("username"))

        object = strack(json_data[1], client=client)
        self.assertEquals(1338, object.get("id"))
        self.assertEquals("Bar", object.get("title"))
        self.assertEquals("bar", object.get("permalink"))
        self.assertEquals("user2", object.get("username"))

        object = strack(json_data[2], client=client)
        self.assertEquals(1339, object.get("id"))
        self.assertEquals("Baz", object.get("title"))
        self.assertEquals("baz", object.get("permalink"))
        self.assertEquals("user3", object.get("username"))

    def test_generate_local_filename(self):
        """ Test generated local filename look like this: {id}-{permalink}.mp3. """
        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertEquals("1337-foo.mp3", object.generate_local_filename())

    def test_generate_local_directory(self):
        """ Test local  directory generated is concatenated with track's username. """
        client = Mock()
        object = strack(json_data[0], client=client)

        dir = object.generate_local_directory("/tmp")
        self.assertEquals("/tmp/user1/", dir)
        if not os.path.exists(dir):
            self.fail("Generate local directory must create directory if not exists.")
        os.rmdir(dir)

    def test_track_not_exists(self):
        """ Test track doesn't exists. """
        os.mkdir("/tmp/user1")
        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertFalse(object.track_exists("/tmp"))
        os.rmdir("/tmp/user1")

    def test_track_exists(self):
        """ Test track exists. """
        os.mkdir("/tmp/user1")
        f = open("/tmp/user1/1337-foo.mp3", "w")
        f.write("0"*5)
        f.close()

        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertTrue(object.track_exists("/tmp"))

        os.remove("/tmp/user1/1337-foo.mp3")
        os.rmdir("/tmp/user1")
