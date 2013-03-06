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
from mock import MagicMock

sys.path.insert(0, "../../")
from ssyncer.suser import suser
from ssyncer.strack import strack


def mock_tracks_response(uri):
    def json_res():
        return b'[{"kind":"track","id":1337,"title":"Foo","permalink":"foo","downloadable":true,"user":{"permalink":"user1"}, "original_format":"mp3"},{"kind":"track","id":1338,"title":"Bar","permalink":"bar","downloadable":true,"user":{"permalink":"user2"}, "original_format":"mp3"},{"kind":"track","id":1339,"title":"Baz","permalink":"baz","downloadable":true,"user":{"permalink":"user3"}, "original_format":"wav"}]'

    response = MagicMock()
    response.read = json_res
    return response


class TestSuser(unittest.TestCase):

    def test_object_has_good_name(self):
        """ Test object has name `foo`. """
        client = Mock()
        object = suser("Foo", client=client)
        self.assertEqual("Foo", object.name)

    def test_parse_tracks_response(self):
        """ Test parse tracks response on success. """
        client = MagicMock()
        object = suser("Foo", client=client)
        tracks = object._parse_tracks_response(mock_tracks_response("bar"))
        self.assertEquals(3, len(tracks))
        for track in tracks:
            self.assertIsInstance(track, strack)

    def test_get_likes_with_default_offset_and_limit(self):
        """ Test get user's likes with default offset and limit. """
        client = MagicMock()
        client.USER_LIKES = "/u/%s/f.json?o=%d&l=%d&c="
        object = suser("Foo", client=client)
        object._parse_tracks_response = Mock()
        object.get_likes()
        client.get.assert_called_once_with(
            "/u/Foo/f.json?o=0&l=50&c=")

    def test_get_likes_with_custom_offset_and_limit(self):
        """ Test get user's likes with custom offset and limit. """
        client = MagicMock()
        client.USER_LIKES = "/u/%s/f.json?o=%d&l=%d&c="
        object = suser("Foo", client=client)
        object._parse_tracks_response = Mock()
        object.get_likes(10, 20)
        client.get.assert_called_once_with(
            "/u/Foo/f.json?o=10&l=20&c=")

    def test_get_tracks_with_default_offset_and_limit(self):
        """ Test get user's tracks with default offset and limit. """
        client = MagicMock()
        client.USER_TRACKS = "/u/%s/t.json?o=%d&l=%d&c="
        object = suser("Foo", client=client)
        object._parse_tracks_response = Mock()
        object.get_tracks()
        client.get.assert_called_once_with(
            "/u/Foo/t.json?o=0&l=50&c=")

    def test_get_tracks_with_custom_offset_and_limit(self):
        """ Test get user's tracks with custom offset and limit. """
        client = MagicMock()
        client.USER_TRACKS = "/u/%s/t.json?o=%d&l=%d&c="
        object = suser("Foo", client=client)
        object._parse_tracks_response = Mock()
        object.get_tracks(10, 20)
        client.get.assert_called_once_with(
            "/u/Foo/t.json?o=10&l=20&c=")
