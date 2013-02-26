#!/usr/bin/env python3.2

from ssyncer.sclient import sclient
from ssyncer.suser import suser

user      = "YOU"
client_id = "YOUR_CLIENT_ID"
local_dir = "OUTPUT_DIRECTORY"

sclient = sclient(client_id)
suser = suser(user, client=sclient)

likes = suser.get_likes()
if not likes:
    print("ERROR: Can't get user's likes!'")
    exit(1)

for strack in likes:
    strack.download(local_dir)
