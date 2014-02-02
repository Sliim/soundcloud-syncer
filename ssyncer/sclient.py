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

import re
import urllib.request
from ssyncer.serror import serror


class sclient:
    host = "api.soundcloud.com"
    port = "443"
    client_id = None

    SC_HOME = "https://www.soundcloud.com"
    DOWNLOAD_URL = "/tracks/%d/download?client_id="
    STREAM_URL = "/tracks/%d/stream?client_id="
    USER_LIKES = "/users/%s/favorites.json?offset=%d&limit=%d&client_id="
    USER_TRACKS = "/users/%s/tracks.json?offset=%d&limit=%d&client_id="
    TRACK_DATA = "/tracks/%s.json?client_id="

    def __init__(self, client_id=None, **kwargs):
        """ Http client initialization. """
        if "host" in kwargs:
            self.host = kwargs.get("host")
        if "port" in kwargs:
            self.port = kwargs.get("port")

        if not client_id:
            print("INFO: Attempt to get client_id..")
            self.client_id = self.get_client_id()
            print("INFO: OK, client_id = %s" % self.client_id)
        else:
            self.client_id = client_id

    def get_protocol(self):
        """ Get protocol from port to use. """
        if self.port == "443":
            return "https"
        return "http"

    def send_request(self, url):
        """ Send a request to given url. """
        while True:
            try:
                return urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                raise serror(
                    "Request `%s` failed (%s:%s)." %
                    (url, e.__class__.__name__, e.code))
            except Exception as e:
                choice = input(serror(
                    "Error occured: %s - Retry? [yN]" % type(e)))
                if choice.strip().lower() != "y":
                    raise serror(e)

    def get(self, uri):
        """ Send a request to given uri. """
        return self.send_request(
            "{0}://{1}:{2}{3}{4}".format(
                self.get_protocol(),
                self.host,
                self.port,
                uri,
                self.client_id
            )
        )

    def get_location(self, uri):
        """ Send a request and get redirected url. """
        return self.get(uri).geturl()

    def get_client_id(self):
        """ Attempt to get client_id from soundcloud homepage. """
        id = re.search(
            "\"clientID\":\"([a-z0-9]*)\"",
            self.send_request(self.SC_HOME).read().decode("utf-8"))

        if not id:
            raise serror("Cannot retrieve client_id.")

        return id.group(1)
