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

import os.path
from ssyncer.sclient import sclient
from ssyncer.strack import strack


class splaylist:
    client = None
    metadata = {}
    tracks = []

    def __init__(self, playlist_data, **kwargs):
        """ Playlist object initialization, load playlist metadata. """
        if "client" in kwargs:
            self.client = kwargs.get("client")
        elif "client_id" in kwargs:
            self.client = sclient(kwargs.get("client_id"))
        else:
            self.client = sclient()

        def map(key, data):
            return str(data[key]) if key in data else ""

        self.metadata = {
            "duration": map("duration", playlist_data),
            "release-day": map("release_day", playlist_data),
            "permalink-url": map("permalink_url", playlist_data),
            "reposts-count": map("reposts_count", playlist_data),
            "genre": map("genre", playlist_data),
            "permalink": map("permalink", playlist_data),
            "purchase-url": map("purchase_url", playlist_data),
            "release-month": map("release_month", playlist_data),
            "description": map("description", playlist_data),
            "uri": map("uri", playlist_data),
            "label-name": map("label_name", playlist_data),
            "tag-list": map("tag_list", playlist_data),
            "release-year": map("release_year", playlist_data),
            "track-count": map("track_count", playlist_data),
            "user-id": map("user_id", playlist_data),
            "last-modified": map("last_modified", playlist_data),
            "license": map("license", playlist_data)
        }

        self.get_tracks(playlist_data)

    def get(self, key):
        """ Get playlist metadata value from a given key. """
        if key in self.metadata:
            return self.metadata[key]
        return None

    def get_tracks(self, playlist_data=None, *args):
        """ Get playlist's tracks. """
        if self.tracks:
            return self.tracks

        if not playlist_data:
            return False

        for track in playlist_data["tracks"]:
            self.tracks.append(strack(track, client=self.client))

    def gen_filename(self):
        """ Generate local filename for this playlist. """
        return "{0}.m3u".format(self.get("permalink"))

    def write_playlist_file(self, localdir):
        """ Check if playlist exists in local directory. """
        path = "{0}/playlists".format(localdir)
        if not os.path.exists(path):
            os.makedirs(path)

        filepath = "{0}/{1}".format(path, self.gen_filename())
        playlist = open(filepath, "w")
        for track in self.get_tracks():
            playlist.write("{0}/{1}.mp3\n".format(
                os.path.abspath(track.gen_localdir(localdir)),
                track.gen_filename()))
        playlist.close()
