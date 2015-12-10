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
import unittest
from mock import Mock

sys.path.insert(0, "../../")

from ssyncer.splaylist import splaylist
from mock_data import playlists_obj


class TestSplaylist(unittest.TestCase):

    def test_metadata(self):
        """
        Test metadata has been loaded from json object
        and get method return metadata value from a given key.
        """
        client = Mock()

        object = splaylist(playlists_obj[0], client=client)
        self.assertEquals("2524859", object.get("duration"))
        self.assertEquals("Monday", object.get("release-day"))
        self.assertEquals("February", object.get("release-month"))
        self.assertEquals("2020", object.get("release-year"))
        self.assertEquals("http://soundcloud.com/5liim/sets/dabass",
                          object.get("permalink-url"))
        self.assertEquals("0", object.get("reposts-count"))
        self.assertEquals("dnb", object.get("genre"))
        self.assertEquals("dabass", object.get("permalink"))
        self.assertEquals("None", object.get("purchase-url"))
        self.assertEquals("My awesome playlist", object.get("description"))
        self.assertEquals("https://api.soundcloud.com/playlists/1337",
                          object.get("uri"))
        self.assertEquals("My Playlist", object.get("label-name"))
        self.assertEquals("awesome", object.get("tag-list"))
        self.assertEquals("42", object.get("track-count"))
        self.assertEquals("1337", object.get("user-id"))
        self.assertEquals("2015/04/22 08:13:52 +0000",
                          object.get("last-modified"))
        self.assertEquals("Beerware", object.get("license"))

    def test_get_unknown_metadata(self):
        """ Test attempt to get an unknown metadata return None. """
        client = Mock()
        object = splaylist(playlists_obj[0], client=client)
        self.assertEquals(None, object.get("unknown"))

    def test_get_tracks_returns_false_when_no_data(self):
        """ Test get_tracks returns False when no data present. """
        client = Mock()
        object = splaylist(playlists_obj[0], client=client)
        self.assertEquals(False, object.get_tracks())

    def test_get_tracks_returns_tracks_attribute(self):
        """ Test get_tracks returns tracks from attribute. """
        client = Mock()
        object = splaylist(playlists_obj[0], client=client)
        object.tracks = "tracks_attribute"
        self.assertEquals("tracks_attribute", object.get_tracks())

    def test_gen_filename(self):
        client = Mock()
        object = splaylist(playlists_obj[0], client=client)
        self.assertEquals("dabass.m3u", object.gen_filename())
