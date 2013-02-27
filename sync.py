#!/usr/bin/env python3.2
import argparse
import os.path

from ssyncer.sclient import sclient
from ssyncer.suser import suser

parser = argparse.ArgumentParser(description="Soundcloud Syncer")
parser.add_argument("-u", "--user", help="Soundcloud user to sync", type=str, required=True)
parser.add_argument("-c", "--client-id", help="Your client id", type=str, required=True)
parser.add_argument("-o", "--output-dir", help="Output directory", type=str, required=True)
args = parser.parse_args()

if not os.path.exists(args.output_dir):
    print("Error: output directory `%s` doesn's exists." % args.output_dir)
    exit(1)

sclient = sclient(args.client_id)
suser = suser(args.user, client=sclient)

likes = suser.get_likes()
if not likes:
    print("ERROR: Can't get user's likes!'")
    exit(2)

for strack in likes:
    print("Start downloading %s.." % strack.get("title"))
    strack.download(args.output_dir)
