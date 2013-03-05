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
import unittest

from mock import Mock
from mock import MagicMock

sys.path.insert(0, "../../")
from ssyncer.suser import suser
from ssyncer.strack import strack

def mock_get_likes_success(uri):
    def json_res():
        return b'[{"kind":"track","id":1337,"title":"Foo","permalink":"foo","downloadable":true,"user":{"permalink":"user1"}},{"kind":"track","id":1338,"title":"Bar","permalink":"bar","downloadable":true,"user":{"permalink":"user2"}},{"kind":"track","id":1339,"title":"Baz","permalink":"baz","downloadable":true,"user":{"permalink":"user3"}}]'

    response = MagicMock()
    response.read = json_res
    return response

class TestSuser(unittest.TestCase):

    def test_object_has_good_name(self):
        """ Test object has name `foo`. """
        client = Mock()
        object = suser("Foo", client=client)
        self.assertEqual("Foo", object.name)

    def test_get_likes_on_success(self):
        """ Test get user's likes when success. """
        client = MagicMock()
        client.get = Mock(side_effect=mock_get_likes_success)
        object = suser("Foo", client=client)

        likes = object.get_likes()
        self.assertEquals(3, len(likes))
        for like in likes:
            self.assertIsInstance(like, strack)

    def test_get_likes_with_default_offset_and_limit(self):
        """ Test get user's likes with default offset and limit. """
        client = MagicMock()
        client.USER_LIKES = "/users/%s/favorites.json?offset=%s&limit=%s&client_id="
        client.get = Mock(side_effect=mock_get_likes_success)
        object = suser("Foo", client=client)

        object.get_likes()
        client.get.assert_called_once_with(
            "/users/Foo/favorites.json?offset=0&limit=50&client_id="
        )

    def test_get_likes_with_custom_offset_and_limit(self):
        """ Test get user's likes with custom offset and limit. """
        client = MagicMock()
        client.USER_LIKES = "/users/%s/favorites.json?offset=%s&limit=%s&client_id="
        client.get = Mock(side_effect=mock_get_likes_success)
        object = suser("Foo", client=client)

        object.get_likes(10, 20)
        client.get.assert_called_once_with(
            "/users/Foo/favorites.json?offset=10&limit=20&client_id="
        )
