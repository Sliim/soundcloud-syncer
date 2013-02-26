import http.client

class sclient:
    host = "api.soundcloud.com"
    port = "443"
    client_id = None
    connection = None

    DOWNLOAD_URL = "/tracks/%s/download?client_id="
    STREAM_URL = "/tracks/%s/stream?client_id="
    USER_LIKES = "/users/%s/favorites.json?client_id="

    def __init__(self, client_id, **kwargs):
        if "host" in kwargs:
            self.host = kwargs.get("host")
        if "port" in kwargs:
            self.port = kwargs.get("port")

        self.client_id = client_id
        self._init_connection(self.host, self.port)

    def _init_connection(self, host, port):
        self.connection = http.client.HTTPSConnection(host, port)

    def _close_connection(self):
        self.connection.close()

    def _reset_connection(self):
        self._close_connection()
        self._init_connection(self.host, self.port)

    def get(self, uri):
        print("DEBUG: Send request to {0}{1}".format(uri, self.client_id))
        try:
            self.connection.request("GET", uri + self.client_id)
            return self.connection.getresponse()
        except http.client.HTTPException as e:
            self._reset_connection()
            print("ERROR: Error occured when sending request `%s` (%s)" % (uri, e.__class__.__name__))
            return False

    def get_location(self, uri):
        response = self.get(uri)
        if not response:
            return False

        response.read()
        return response.getheader("Location")
