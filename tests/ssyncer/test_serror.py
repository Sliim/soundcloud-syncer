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

sys.path.insert(0, "../../")
from ssyncer.serror import serror


class TestSerror(unittest.TestCase):

    def test_init(self):
        """ Test exception initialization. """
        serr = serror("foo")
        self.assertEquals("foo", serr.message)

    def test_to_string(self):
        """ Test exception string representation. """
        serr = serror("bar")
        self.assertEquals("\033[91mERROR: bar\033[0m", serr.__str__())
