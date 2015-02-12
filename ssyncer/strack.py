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
import re
from dateutil.parser import parse

from ssyncer.sclient import sclient
from ssyncer.serror import serror

from stagger.id3 import *
from stagger.tags import Tag24

from pydub import AudioSegment


class strack:

    client = None
    metadata = {}
    downloaded = False
    filename = None

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

    def download(self, localdir, max_retry):
        """ Download a track in local directory. """
        local_file = self.gen_localdir(localdir) + self.gen_filename()

        if self.track_exists(localdir):
            print("Track {0} already downloaded, skipping!".format(
                self.get("id")))
            return False

        if local_file in self.get_ignored_tracks(localdir):
            print("\033[93mTrack {0} ignored, skipping!!\033[0m".format(
                self.get("id")))
            return False

        dlurl = self.get_download_link()

        if not dlurl:
            raise serror("Can't download track_id:%d|%s" % (
                self.get("id"),
                self.get("title")))

        retry = max_retry
        print("\nDownloading %s (%d).." % (self.get("title"), self.get("id")))

        while True:
            try:
                urllib.request.urlretrieve(dlurl, local_file,
                                           self._progress_hook)
                break
            except Exception as e:
                if os.path.isfile(local_file):
                    os.unlink(local_file)
                retry -= 1

                if retry < 0:
                    raise serror("Can't download track-id %s, max retry "
                                 "reached (%d). Error occured: %s" % (
                                     self.get("id"), max_retry, type(e)))
                else:
                    print("\033[93mError occured for track-id %s (%s). "
                          "Retrying.. (%d/%d) \033[0m" % (
                              self.get("id"),
                              type(e),
                              max_retry - retry,
                              max_retry))
            except KeyboardInterrupt:
                if os.path.isfile(local_file):
                    os.unlink(local_file)
                raise serror("KeyBoard Interrupt: Incomplete file removed.")

        self.filepath = local_file + self.get_file_extension(local_file)
        os.rename(local_file, self.filepath)
        print("Downloaded => %s" % self.filepath)

        self.downloaded = True
        return True

    def process_tags(self, tag=None):
        """Process ID3 Tags for mp3 files."""
        if self.downloaded is False:
            raise serror("Track not downloaded, can't process tags..")
        if magic.from_file(self.filepath, mime=True) != b"audio/mpeg":
            return False

        print("Processing tags for %s.." % self.filepath)
        if tag is None:
            tag = stag()
        tag.load_id3(self)
        tag.write_id3(self.filepath)

    def convert(self):
        """Convert file in mp3 format."""
        if self.downloaded is False:
            raise serror("Track not downloaded, can't convert file..")
        if magic.from_file(self.filepath, mime=True) == b"audio/mpeg":
            return False

        rootpath = os.path.dirname(os.path.dirname(self.filepath))
        backupdir = rootpath + "/backups/" + self.get("username")
        if not os.path.exists(backupdir):
            os.makedirs(backupdir)

        backupfile = "%s/%s%s" % (
            backupdir,
            self.gen_filename(),
            self.get_file_extension(self.filepath))
        newfile = "%s.mp3" % self.filename_without_extension()

        os.rename(self.filepath, backupfile)
        self.filepath = newfile

        print("Converting to %s.." % newfile)
        song = AudioSegment.from_file(backupfile)
        return song.export(newfile, format="mp3")

    def filename_without_extension(self):
        """Return filename without extension"""
        return re.sub("\.\w+$", "", self.filepath)

    def download_artwork(self, localdir, max_retry):
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
                os.unlink(artwork_dir)
            os.mkdir(artwork_dir)

        artwork_filepath = artwork_dir + "/" + self.gen_artwork_filename()

        retry = max_retry
        while True:
            try:
                res = urllib.request.urlopen(self.get("artwork-url"))
                with open(artwork_filepath, "wb") as file:
                    file.write(res.read())
                break
            except Exception as e:
                retry -= 1
                if retry < 0:
                    print(serror("Can't download track's artwork, max retry "
                                 "reached (%d). Error occured: %s" % (
                                     max_retry, type(e))))
                    return False
                else:
                    print("\033[93mTrack's artwork download failed (%s). "
                          "Retrying.. (%d/%d) \033[0m" % (
                              type(e),
                              max_retry - retry,
                              max_retry))

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
