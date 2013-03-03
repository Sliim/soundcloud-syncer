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

from ssyncer.sclient import sclient
from ssyncer.strack import strack
import json

class suser:

    name = None
    client = None

    def __init__(self, username, **kwargs):
        """ Initialize soundcloud's user object. """
        self.name = username

        if "client" in kwargs:
            self.client = kwargs.get("client")
        elif "client_id" in kwargs:
            self.client = sclient(kwargs.get("client_id"))
        else:
            raise Exception("client or client_id missing..")

    def get_likes(self, offset=0, limit=50):
        """ Get user's likes. """
        response = self.client.get(self.client.USER_LIKES % (self.name, offset, limit))
        if not response:
            return False

        tracks = json.loads(response.read().decode("utf-8"))
        likes = []

        for track in tracks:
            likes.append(strack(track, client=self.client))

        return likes
