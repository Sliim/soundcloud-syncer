from ssyncer.sclient import sclient
from ssyncer.strack import strack
import json

class suser:

    name = None
    client = None

    def __init__(self, username, **kwargs):
        """ Initialize soundcloud's user object. """
        self.name = username

        if "client" in kwargs:
            self.client = kwargs.get("client")
        elif "client_id" in kwargs:
            self.client = sclient(kwargs.get("client_id"))
        else:
            raise Exception("client or client_id missing..")

    def get_likes(self):
        """ Get user's likes. """
        response = self.client.get(self.client.USER_LIKES % self.name)
        if not response:
            return False

        tracks = json.loads(response.read().decode("utf-8"))
        likes = []

        for track in tracks:
            likes.append(strack(track, client=self.client))

        return likes
