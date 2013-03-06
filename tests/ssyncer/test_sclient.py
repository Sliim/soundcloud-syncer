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
from ssyncer.sclient import sclient


class TestSclient(unittest.TestCase):

    def test_init(self):
        """ Test basic object initialization. """
        object = sclient("my_id")
        self.assertEquals("my_id", object.client_id)

    def test_init_auto_get_client_id(self):
        """
        Test object init get automatically client_id
        when not passed in args.
        """
        sclient.get_client_id = Mock()
        sclient()
        sclient.get_client_id.assert_called_once()

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
