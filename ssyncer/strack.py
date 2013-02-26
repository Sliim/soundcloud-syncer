from ssyncer.sclient import sclient
import os.path
import urllib.request

class strack:

    client = None
    metadata = {}

    def __init__(self, track_data, **kwargs):
        self.metadata = {
            "id": track_data["id"],
            "title": track_data["title"],
            "permalink": track_data["permalink"],
            "username": track_data["user"]["permalink"]
        }

        if "client" in kwargs:
            self.client = kwargs.get("client")
        elif "client_id" in kwargs:
            self.client = sclient(kwargs.get("client_id"))
        else:
            raise Exception("client or client_id missing..")

    def get(self, key):
        if key in self.metadata:
            return self.metadata[key]
        return None

    def get_download_link(self):
        url = self.client.get_location(self.client.DOWNLOAD_URL % self.get("id"))
        if not url:
            url = self.client.get_location(self.client.STREAM_URL % self.get("id"))
        return url

    def generate_local_filename(self):
        return "{0}-{1}.mp3".format(self.get("id"), self.get("permalink"))

    def generate_local_directory(self, local_dir):
        directory = "{0}/{1}/".format(local_dir, self.get("username"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def track_exists(self, local_dir):
        path = self.generate_local_directory(local_dir) + self.generate_local_filename()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        return False

    def download(self, local_dir):
        local_file = self.generate_local_directory(local_dir) + self.generate_local_filename()

        if self.track_exists(local_dir):
            print("INFO: Track {0} already downloaded, skipping!".format(self.get("id")))
            return False

        dlurl = self.get_download_link()
        if not dlurl:
            print("ERROR: Can't download track_id:{0}|{1}".format(
                self.get("id"),
                self.get("title")
            ))
            return False

        r = urllib.request.urlopen(dlurl)
        f = open(local_file, "bw")
        f.write(r.read())
        f.close()
