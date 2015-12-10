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

from ssyncer.sclient import sclient
from ssyncer.strack import strack
from ssyncer.splaylist import splaylist
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
            self.client = sclient()

    def get_likes(self, offset=0, limit=50):
        """ Get user's likes. """
        response = self.client.get(
            self.client.USER_LIKES % (self.name, offset, limit))
        return self._parse_response(response, strack)

    def get_tracks(self, offset=0, limit=50):
        """ Get user's tracks. """
        response = self.client.get(
            self.client.USER_TRACKS % (self.name, offset, limit))
        return self._parse_response(response, strack)

    def get_playlists(self, offset=0, limit=50):
        """ Get user's playlists. """
        response = self.client.get(
            self.client.USER_PLAYLISTS % (self.name, offset, limit))
        return self._parse_response(response, splaylist)

        return playlists

    def _parse_response(self, response, target_object=strack):
        """ Generic response parser method """
        objects = json.loads(response.read().decode("utf-8"))
        list = []
        for obj in objects:
            list.append(target_object(obj, client=self.client))
        return list
