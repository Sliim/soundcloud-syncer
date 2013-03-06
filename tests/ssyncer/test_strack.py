# This source file is part of Soundcloud-syncer.
#
# Soundcloud-syncer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Soundcloud-syncer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Soundcloud-syncer. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import sys
import os
import json
import unittest
from mock import Mock

sys.path.insert(0, "../../")
from ssyncer.strack import strack

json_data = json.loads('[{"kind":"track","id":1337,"title":"Foo","permalink":"foo","downloadable":true,"user":{"permalink":"user1"}, "original_format":"mp3"},{"kind":"track","id":1338,"title":"Bar","permalink":"bar","downloadable":false,"user":{"permalink":"user2"}, "original_format":"mp3"},{"kind":"track","id":1339,"title":"Baz","permalink":"baz","downloadable":true,"user":{"permalink":"user3"}, "original_format":"wav"}]')

class TestStrack(unittest.TestCase):

    tmpdir = "/tmp/stests"

    def setUp(self):
        """ Create temporary directory for tests. """
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)

    def tearDown(self):
        """ This testsuite create temporary dir/files. Delete them after each tests. """
        if os.path.exists("%s/user1/1337-foo.mp3" % self.tmpdir):
            os.remove("%s/user1/1337-foo.mp3" % self.tmpdir)
        if os.path.exists("%s/user1" % self.tmpdir):
            os.rmdir("%s/user1" % self.tmpdir)
        if os.path.exists("%s/.ignore" % self.tmpdir):
            os.remove("%s/.ignore" % self.tmpdir)
        if os.path.exists(self.tmpdir):
            os.rmdir(self.tmpdir)

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
        self.assertTrue(object.get("downloadable"))
        self.assertEquals("mp3", object.get("ext"))

        object = strack(json_data[1], client=client)
        self.assertEquals(1338, object.get("id"))
        self.assertEquals("Bar", object.get("title"))
        self.assertEquals("bar", object.get("permalink"))
        self.assertEquals("user2", object.get("username"))
        self.assertFalse(object.get("downloadable"))
        self.assertEquals("mp3", object.get("ext"))

        object = strack(json_data[2], client=client)
        self.assertEquals(1339, object.get("id"))
        self.assertEquals("Baz", object.get("title"))
        self.assertEquals("baz", object.get("permalink"))
        self.assertEquals("user3", object.get("username"))
        self.assertTrue(object.get("downloadable"))
        self.assertEquals("wav", object.get("ext"))

    def test_get_unknown_metadata(self):
        """ Test attempt to get an unknown metadata return None. """
        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertEquals(None, object.get("unknown"))

    def test_get_download_link(self):
        """ Test get download link. """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%s"
        client.STREAM_URL = "mock_stream_url_%s"
        client.get_location.return_value = "http://lost.iya"

        object = strack(json_data[0], client=client)
        self.assertEquals("http://lost.iya", object.get_download_link())
        client.get_location.assert_called_once_with("mock_download_url_1337")
        self.assertEquals(1 , client.get_location.call_count)

    def test_get_download_link_not_downloadable(self):
        """ Test get download link from stream url. """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%s"
        client.STREAM_URL = "mock_stream_url_%s"
        client.get_location.return_value = "http://lost.iya"

        object = strack(json_data[1], client=client)
        self.assertEquals("http://lost.iya", object.get_download_link())
        client.get_location.assert_called_with("mock_stream_url_1338")
        self.assertEquals(1 , client.get_location.call_count)

    def test_get_download_link_not_downloadable_and_streamable(self):
        """ Test that get_download_link method return None when track isn't downloadble and streamable. """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%s"
        client.STREAM_URL = "mock_stream_url_%s"
        client.get_location = Mock()
        client.get_location.return_value = None

        object = strack(json_data[1], client=client)
        self.assertEquals(None, object.get_download_link())
        client.get_location.assert_called_with("mock_download_url_1338")
        self.assertEquals(2 , client.get_location.call_count)

    def test_generate_local_filename(self):
        """ Test generated local filename look like this: {id}-{permalink}.{ext}. """
        client = Mock()
        object = strack(json_data[2], client=client)
        self.assertEquals("1339-baz.wav", object.generate_local_filename())

    def test_generate_local_directory(self):
        """ Test local  directory generated is concatenated with track's username. """
        client = Mock()
        object = strack(json_data[0], client=client)

        dir = object.generate_local_directory(self.tmpdir)
        self.assertEquals("%s/user1/" % self.tmpdir, dir)
        if not os.path.exists(dir):
            self.fail("Generate local directory must create directory if not exists.")
        os.rmdir(dir)

    def test_track_not_exists(self):
        """ Test track doesn't exists. """
        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertFalse(object.track_exists(self.tmpdir))

    def test_track_exists(self):
        """ Test track exists. """
        os.mkdir("%s/user1" % self.tmpdir)
        f = open("%s/user1/1337-foo.mp3" % self.tmpdir, "w")
        f.write("0"*5)
        f.close()

        client = Mock()
        object = strack(json_data[0], client=client)
        self.assertTrue(object.track_exists(self.tmpdir))

    def test_get_track_ignored(self):
        """ Test get track ignored list. """
        f = open("%s/.ignore" % self.tmpdir, "w")
        f.write("foo\nbar\nbaz")
        f.close()

        client = Mock()
        object = strack(json_data[0], client=client)
        ignored = object.get_ignored_tracks(self.tmpdir)
        self.assertIn("%s/foo" % self.tmpdir, ignored)
        self.assertIn("%s/bar" % self.tmpdir, ignored)
        self.assertIn("%s/baz" % self.tmpdir, ignored)

    def test_get_track_ignored_not_ignore_file(self):
        """ Test get track ignored list when ignore file doesn't exists. """
        client = Mock()
        object = strack(json_data[0], client=client)
        ignored = object.get_ignored_tracks(self.tmpdir)
        self.assertEquals(0, len(ignored))
