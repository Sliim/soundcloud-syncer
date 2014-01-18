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
# You should have received a copy of the GNU General Public License along with
# Soundcloud-syncer. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import sys
import os
import unittest
from mock import Mock

sys.path.insert(0, "../../")
from ssyncer.strack import strack, stag
from mock_data import json_obj

from stagger.id3 import *


class TestStrack(unittest.TestCase):

    tmpdir = "/tmp/stests"

    def setUp(self):
        """ Create temporary directory for tests. """
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)

    def tearDown(self):
        """
        This testsuite create temporary dir/files.
        Delete them after each tests.
        """
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

        object = strack(json_obj[0], client=client)
        self.assertEquals(1337, object.get("id"))
        self.assertEquals("Foo", object.get("title"))
        self.assertEquals("foo", object.get("permalink"))
        self.assertEquals("user1", object.get("username"))
        self.assertEquals("http://user1.dev", object.get("user-url"))
        self.assertTrue(object.get("downloadable"))
        self.assertEquals("mp3", object.get("original-format"))
        self.assertEquals("247010", object.get("duration"))
        self.assertEquals("9931892", object.get("original-content-size"))
        self.assertEquals("dubstep bass", object.get("tags-list"))
        self.assertEquals("Dubstep", object.get("genre"))
        self.assertEquals("Some text", object.get("description"))
        self.assertEquals("free", object.get("license"))
        self.assertEquals("https://api.foobar.dev/1337", object.get("uri"))
        self.assertEquals("2013/12/18 13:37:00 +0000",
                          object.get("created-at"))
        self.assertEquals("https://foobar.dev/1337",
                          object.get("permalink-url"))
        self.assertEquals("https://foobar.dev/1337-crop.jpg",
                          object.get("artwork-url"))

        object = strack(json_obj[1], client=client)
        self.assertEquals(1338, object.get("id"))
        self.assertEquals("Bar", object.get("title"))
        self.assertEquals("bar", object.get("permalink"))
        self.assertEquals("user2", object.get("username"))
        self.assertEquals("http://user2.dev", object.get("user-url"))
        self.assertFalse(object.get("downloadable"))
        self.assertEquals("mp3", object.get("original-format"))
        self.assertEquals("247011", object.get("duration"))
        self.assertEquals("9931893", object.get("original-content-size"))
        self.assertEquals("trap bass", object.get("tags-list"))
        self.assertEquals("Trap", object.get("genre"))
        self.assertEquals("Some description", object.get("description"))
        self.assertEquals("Common", object.get("license"))
        self.assertEquals("https://api.foobar.dev/1338", object.get("uri"))
        self.assertEquals("2013/12/18 13:37:01 +0000",
                          object.get("created-at"))
        self.assertEquals("https://foobar.dev/1338",
                          object.get("permalink-url"))
        self.assertEquals("https://foobar.dev/1338-crop.jpg",
                          object.get("artwork-url"))

        object = strack(json_obj[2], client=client)
        self.assertEquals(1339, object.get("id"))
        self.assertEquals("Baz", object.get("title"))
        self.assertEquals("baz", object.get("permalink"))
        self.assertEquals("user3", object.get("username"))
        self.assertEquals("http://user3.dev", object.get("user-url"))
        self.assertTrue(object.get("downloadable"))
        self.assertEquals("wav", object.get("original-format"))
        self.assertEquals("247012", object.get("duration"))
        self.assertEquals("9931894", object.get("original-content-size"))
        self.assertEquals("drumandbass bass", object.get("tags-list"))
        self.assertEquals("D&B", object.get("genre"))
        self.assertEquals("Awesome D&B", object.get("description"))
        self.assertEquals("copyleft", object.get("license"))
        self.assertEquals("https://api.foobar.dev/1339", object.get("uri"))
        self.assertEquals("2013/12/18 13:37:02 +0000",
                          object.get("created-at"))
        self.assertEquals("https://foobar.dev/1339",
                          object.get("permalink-url"))
        self.assertEquals("https://foobar.dev/1339-crop.jpg",
                          object.get("artwork-url"))

    def test_get_unknown_metadata(self):
        """ Test attempt to get an unknown metadata return None. """
        client = Mock()
        object = strack(json_obj[0], client=client)
        self.assertEquals(None, object.get("unknown"))

    def test_get_download_link(self):
        """ Test get download link. """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%d"
        client.STREAM_URL = "mock_stream_url_%d"
        client.get_location.return_value = "http://lost.iya"

        object = strack(json_obj[0], client=client)
        self.assertEquals("http://lost.iya", object.get_download_link())
        client.get_location.assert_called_once_with("mock_download_url_1337")
        self.assertEquals(1, client.get_location.call_count)

    def test_get_download_link_not_downloadable(self):
        """ Test get download link from stream url. """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%d"
        client.STREAM_URL = "mock_stream_url_%d"
        client.get_location.return_value = "http://lost.iya"

        object = strack(json_obj[1], client=client)
        self.assertEquals("http://lost.iya", object.get_download_link())
        client.get_location.assert_called_with("mock_stream_url_1338")
        self.assertEquals(1, client.get_location.call_count)

    def test_get_download_link_not_downloadable_and_streamable(self):
        """
        Test that get_download_link method return None
        when track isn't downloadble and streamable.
        """
        client = Mock()
        client.DOWNLOAD_URL = "mock_download_url_%d"
        client.STREAM_URL = "mock_stream_url_%d"
        client.get_location = Mock()
        client.get_location.return_value = None

        object = strack(json_obj[1], client=client)
        self.assertEquals(None, object.get_download_link())
        client.get_location.assert_called_with("mock_download_url_1338")
        self.assertEquals(2, client.get_location.call_count)

    def test_gen_filename(self):
        """
        Test generated local filename look like this:
        {id}-{permalink}.{ext}.
        """
        client = Mock()
        object = strack(json_obj[2], client=client)
        self.assertEquals("1339-baz.wav", object.gen_filename())

    def test_gen_localdir(self):
        """
        Test local  directory generated is
        concatenated with track's username.
        """
        client = Mock()
        object = strack(json_obj[0], client=client)

        dir = object.gen_localdir(self.tmpdir)
        self.assertEquals("%s/user1/" % self.tmpdir, dir)
        if not os.path.exists(dir):
            self.fail("Generate local directory must create it if not exists.")
        os.rmdir(dir)

    def test_track_not_exists(self):
        """ Test track doesn't exists. """
        client = Mock()
        object = strack(json_obj[0], client=client)
        self.assertFalse(object.track_exists(self.tmpdir))

    def test_track_exists(self):
        """ Test track exists. """
        os.mkdir("%s/user1" % self.tmpdir)
        f = open("%s/user1/1337-foo.mp3" % self.tmpdir, "w")
        f.write("0" * 5)
        f.close()

        client = Mock()
        object = strack(json_obj[0], client=client)
        self.assertTrue(object.track_exists(self.tmpdir))

    def test_get_track_ignored(self):
        """ Test get track ignored list. """
        f = open("%s/.ignore" % self.tmpdir, "w")
        f.write("foo\nbar\nbaz")
        f.close()

        client = Mock()
        object = strack(json_obj[0], client=client)
        ignored = object.get_ignored_tracks(self.tmpdir)
        self.assertIn("%s/foo" % self.tmpdir, ignored)
        self.assertIn("%s/bar" % self.tmpdir, ignored)
        self.assertIn("%s/baz" % self.tmpdir, ignored)

    def test_get_track_ignored_not_ignore_file(self):
        """ Test get track ignored list when ignore file doesn't exists. """
        client = Mock()
        object = strack(json_obj[0], client=client)
        ignored = object.get_ignored_tracks(self.tmpdir)
        self.assertEquals(0, len(ignored))


class TestStag(unittest.TestCase):

    def test_init_object(self):
        """ Test init stag object"""
        tag = stag()
        from stagger.tags import Tag24
        self.assertIsInstance(tag.mapper, Tag24)

    def test_load_id3(self):
        """ Test load id3 tags """
        tag = stag()
        client = Mock()

        track = strack(json_obj[0], client=client)

        tag.load_id3(track)

        self.assertEqual("Some text", tag.mapper._frames["TIT1"][0].text[0])
        self.assertEqual("Foo", tag.mapper._frames["TIT2"][0].text[0])
        self.assertEqual("dubstep bass", tag.mapper._frames["TIT3"][0].text[0])
        self.assertEqual("2013", tag.mapper._frames["TYER"][0].text[0])
        self.assertEqual("1812", tag.mapper._frames["TDAT"][0].text[0])
        self.assertEqual("1337", tag.mapper._frames["TIME"][0].text[0])
        self.assertEqual("247010", tag.mapper._frames["TLEN"][0].text[0])
        self.assertEqual("9931892", tag.mapper._frames["TSIZ"][0].text[0])
        self.assertEqual("foo", tag.mapper._frames["TOFN"][0].text[0])
        self.assertEqual("Dubstep", tag.mapper._frames["TCON"][0].text[0])
        self.assertEqual("free", tag.mapper._frames["TCOP"][0].text[0])
        self.assertEqual("https://foobar.dev/1337",
                         tag.mapper._frames["WOAS"][0].url)
        self.assertEqual("https://api.foobar.dev/1337",
                         tag.mapper._frames["WOAF"][0].url)
        self.assertEqual("user1", tag.mapper._frames["TPUB"][0].text[0])
        self.assertEqual("http://user1.dev",
                         tag.mapper._frames["WOAR"][0].url)
        #self.assertIn("APIC", tag.mapper._frames)

    def test_load_id3_requires_strack_obj(self):
        """ Test load_id3 raise exception when strack is invalid object """
        tag = stag()
        track = Mock()
        self.assertRaises(TypeError, tag.load_id3, track)
