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
import os.path
import urllib.request

from ssyncer.sclient import sclient
from ssyncer.serror import serror


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
            "downloadable": track_data["downloadable"],
            "ext": track_data["original_format"],
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
                url = self.client.get_location(
                    self.client.STREAM_URL % self.get("id"))
            except serror as e:
                print(e)

        if not url:
            try:
                url = self.client.get_location(
                    self.client.DOWNLOAD_URL % self.get("id"))
            except serror as e:
                print(e)

        return url

    def gen_filename(self):
        """ Generate local filename for this track. """
        return "{0}-{1}.{2}".format(
            self.get("id"),
            self.get("permalink"),
            self.get("ext"))

    def gen_localdir(self, localdir):
        """
        Generate local directory where track will be saved.
        Create it if not exists.
        """
        directory = "{0}/{1}/".format(localdir, self.get("username"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def track_exists(self, localdir):
        """ Check if track exists in local directory. """
        path = self.gen_localdir(localdir) + self.gen_filename()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        return False

    def get_ignored_tracks(self, localdir):
        """ Get ignored tracks list. """
        ignore_file = "%s/.ignore" % localdir
        list = []
        if os.path.exists(ignore_file):
            f = open(ignore_file)
            ignored = f.readlines()
            f.close()

            for i in ignored:
                list.append("%s/%s" % (localdir, i.rstrip()))

        return list

    def download(self, localdir):
        """ Download a track in local directory. """
        local_file = self.gen_localdir(localdir) + self.gen_filename()

        if self.track_exists(localdir):
            print("INFO: Track {0} already downloaded, skipping!".format(
                self.get("id")))
            return False

        if local_file in self.get_ignored_tracks(localdir):
            print("\033[93mINFO: Track {0} ignored, skipping!!\033[0m".format(
                self.get("id")))
            return False

        dlurl = self.get_download_link()

        if not dlurl:
            raise serror("Can't download track_id:%d|%s" % (
                self.get("id"),
                self.get("title")))

        try:
            print("Start downloading %s (%d).." % (
                self.get("title"),
                self.get("id")))
            urllib.request.urlretrieve(dlurl, local_file, self._progress_hook)
        except:
            os.remove(local_file)
            raise

    def _progress_hook(self, blocknum, blocksize, totalsize):
        """ Progress hook for urlretrieve. """
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), read, totalsize)
            sys.stderr.write(s)

            if read >= totalsize:
                sys.stderr.write("\n")
        else:
            sys.stderr.write("read %d\n" % read)
