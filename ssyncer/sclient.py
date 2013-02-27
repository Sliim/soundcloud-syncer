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

import urllib.request

class sclient:
    host = "api.soundcloud.com"
    port = "443"
    client_id = None

    DOWNLOAD_URL = "/tracks/%s/download?client_id="
    STREAM_URL = "/tracks/%s/stream?client_id="
    USER_LIKES = "/users/%s/favorites.json?client_id="

    def __init__(self, client_id, **kwargs):
        """ Http client initialization. """
        if "host" in kwargs:
            self.host = kwargs.get("host")
        if "port" in kwargs:
            self.port = kwargs.get("port")

        self.client_id = client_id

    def get_protocol(self):
        """ Get protocol from port to use. """
        if self.port == "443":
            return "https"
        return "http"

    def send_request(self, url):
        """ Send a request to given url. """
        try:
            return urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print("ERROR: In request `%s` (%s)" % (url, e.__class__.__name__))
            return False

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
        res = self.get(uri)
        if not res:
            return False
        return res.geturl()
