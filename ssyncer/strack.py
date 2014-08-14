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
import calendar
import tempfile
import glob
import magic
from dateutil.parser import parse

from ssyncer.sclient import sclient
from ssyncer.serror import serror

from stagger.id3 import *
from stagger.tags import Tag24


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

        def map(key, data):
            return str(data[key]) if key in data else ""

        self.metadata = {
            "id": track_data["id"],
            "title": map("title", track_data),
            "permalink": map("permalink", track_data),
            "username": map("permalink", track_data["user"]),
            "artist": map("username", track_data["user"]),
            "user-url": map("permalink_url", track_data["user"]),
            "downloadable": track_data["downloadable"],
            "original-format": map("original_format", track_data),
            "created-at": map("created_at", track_data),
            "duration": map("duration", track_data),
            "tags-list": map("tags_list", track_data),
            "genre": map("genre", track_data),
            "description": map("description", track_data),
            "license": map("license", track_data),
            "uri": map("uri", track_data),
            "permalink-url": map("permalink_url", track_data),
            "artwork-url": map("artwork_url",
                               track_data).replace("large", "crop"),
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
        return "{0}-{1}".format(
            self.get("id"),
            self.get("permalink"))

    def get_file_extension(self, filepath):
        """
        This method check mimetype to define file extension.
        If it can't, it use original-format metadata.
        """
        mtype = magic.from_file(filepath, mime=True)
        if mtype == b"audio/mpeg":
            ext = ".mp3"
        elif mtype == b"audio/x-wav":
            ext = ".wav"
        else:
            ext = "." + self.get("original-format")
        return ext

    def gen_artwork_filename(self):
        """ Generate artwork filename for cover of this track. """
        return "{0}-{1}.jpg".format(
            self.get("id"),
            self.get("permalink"))

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
        path = glob.glob(self.gen_localdir(localdir)
                         + self.gen_filename()
                         + "*")
        if len(path) > 0 and os.path.getsize(path[0]) > 0:
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

    def download(self, localdir, process_tag=True):
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

        local_file_with_ext = local_file + self.get_file_extension(local_file)
        os.rename(local_file, local_file_with_ext)
        print("Downloaded => %s\n" % local_file_with_ext)

        self.download_artwork(localdir)

        if process_tag and local_file_with_ext[-3:] == "mp3":
            tag = stag()
            tag.load_id3(self)
            tag.write_id3(local_file_with_ext)

    def download_artwork(self, localdir):
        """
        Download track's artwork and return file path.
        Artwork's path is saved in track's metadata as 'artwork-path' key.
        """
        if self.get("artwork-url") == "None":
            self.metadata["artwork-path"] = None
            return None

        artwork_dir = localdir + "/artworks"
        if not os.path.isdir(artwork_dir):
            if os.path.isfile(artwork_dir):
                os.path.remove(artwork_dir)
            os.mkdir(artwork_dir)

        artwork_filepath = artwork_dir + "/" + self.gen_artwork_filename()
        res = urllib.request.urlopen(self.get("artwork-url"))
        with open(artwork_filepath, "wb") as file:
            file.write(res.read())

        self.metadata["artwork-path"] = artwork_filepath

    def _progress_hook(self, blocknum, blocksize, totalsize):
        """ Progress hook for urlretrieve. """
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 1e2 / totalsize
            s = "\r%d%% %*d / %d" % (
                percent, len(str(totalsize)), read, totalsize)
            sys.stdout.write(s)

            if read >= totalsize:
                sys.stdout.write("\n")
        else:
            sys.stdout.write("read %d\n" % read)


class stag:
    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()
        self.mapper = Tag24()

    def load_id3(self, track):
        """ Load id3 tags from strack metadata """
        if not isinstance(track, strack):
            raise TypeError('strack object required')

        timestamp = calendar.timegm(parse(track.get("created-at")).timetuple())

        self.mapper[TIT1] = TIT1(text=track.get("description"))
        self.mapper[TIT2] = TIT2(text=track.get("title"))
        self.mapper[TIT3] = TIT3(text=track.get("tags-list"))
        self.mapper[TDOR] = TDOR(text=str(timestamp))
        self.mapper[TLEN] = TLEN(text=track.get("duration"))
        self.mapper[TOFN] = TOFN(text=track.get("permalink"))
        self.mapper[TCON] = TCON(text=track.get("genre"))
        self.mapper[TCOP] = TCOP(text=track.get("license"))
        self.mapper[WOAS] = WOAS(url=track.get("permalink-url"))
        self.mapper[WOAF] = WOAF(url=track.get("uri"))
        self.mapper[TPUB] = TPUB(text=track.get("username"))
        self.mapper[WOAR] = WOAR(url=track.get("user-url"))
        self.mapper[TPE1] = TPE1(text=track.get("artist"))
        self.mapper[TALB] = TALB(text="%s Soundcloud tracks"
                                 % track.get("artist"))

        if track.get("artwork-path") is not None:
            self.mapper[APIC] = APIC(value=track.get("artwork-path"))

    def write_id3(self, filename):
        """ Write id3 tags """
        if not os.path.exists(filename):
            raise ValueError("File doesn't exists.")

        self.mapper.write(filename)
