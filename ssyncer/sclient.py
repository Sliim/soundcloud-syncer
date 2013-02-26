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
