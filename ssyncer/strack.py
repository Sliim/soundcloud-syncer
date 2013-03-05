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
from ssyncer.serror import serror

import os.path

class strack:

    client = None
    metadata = {}

    def __init__(self, track_data, **kwargs):
        """ Track object initialization, load track metadata. """
        if "client" in kwargs:
            self.client = kwargs.get("client")
        elif "client_id" in kwargs:
            self.client = sclient(kwargs.get("client_id"))
        else:
            self.client = sclient()

        self.metadata = {
            "id": track_data["id"],
            "title": track_data["title"],
            "permalink": track_data["permalink"],
            "username": track_data["user"]["permalink"],
            "downloadable": track_data["downloadable"]
        }

    def get(self, key):
        """ Get track metadata value from a given key. """
        if key in self.metadata:
            return self.metadata[key]
        return None

    def get_download_link(self):
        """ Get direct download link with soudcloud's redirect system. """
        url = None
        if not self.get("downloadable"):
            try:
                url = self.client.get_location(self.client.STREAM_URL % self.get("id"))
            except serror as e:
                print(e)

        if not url:
            try:
                url = self.client.get_location(self.client.DOWNLOAD_URL % self.get("id"))
            except serror as e:
                print(e)

        return url

    def generate_local_filename(self):
        """ Generate local filename for this track. """
        return "{0}-{1}.mp3".format(self.get("id"), self.get("permalink"))

    def generate_local_directory(self, local_dir):
        """ Generate local directory where track will be saved. Create it if not exists. """
        directory = "{0}/{1}/".format(local_dir, self.get("username"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def track_exists(self, local_dir):
        """ Check if track exists in local directory. """
        path = self.generate_local_directory(local_dir) + self.generate_local_filename()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        return False

    def download(self, local_dir):
        """ Download a track in local directory. """
        local_file = self.generate_local_directory(local_dir) + self.generate_local_filename()

        if self.track_exists(local_dir):
            print("INFO: Track {0} already downloaded, skipping!".format(self.get("id")))
            return False

        dlurl = self.get_download_link()

        if not dlurl:
            raise serror("Can't download track_id:%s|%s" % (self.get("id"), self.get("title")))

        r = self.client.send_request(dlurl)
        f = open(local_file, "bw")
        f.write(r.read())
        f.close()
