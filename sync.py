#!/usr/bin/env python3.2
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

import argparse
import os.path

from ssyncer.sclient import sclient
from ssyncer.suser import suser
from ssyncer.serror import serror

parser = argparse.ArgumentParser(description="Soundcloud Syncer")
parser.add_argument("-u", "--user", help="Soundcloud user to sync", type=str, required=True)
parser.add_argument("-c", "--client-id", help="Your client id", type=str)
parser.add_argument("-o", "--output-dir", help="Output directory", type=str, required=True)
parser.add_argument("-O", "--offset", help="Tracks offset", type=int)
parser.add_argument("-L", "--limit", help="Tracks limit (max: 200)", type=int)
parser.add_argument("-r", "--recursive", help="Recursive download", action="store_true")
parser.add_argument("-t", "--tracks", help="Download user's tracks instead user's likes", action="store_true")


def downloader(tgetter, output, *args):
    """ Download tracks. Return number of tracks downloaded. """
    try:
        tracks = tgetter(*args)
    except serror as e:
        print(e)
        return False

    for strack in tracks:
        try:
            strack.download(output)
        except serror as e:
            print(e)

    return len(tracks)

args = parser.parse_args()

if not os.path.exists(args.output_dir):
    print(serror("Error: output directory `%s` doesn's exists." %
                 args.output_dir))
    exit(1)

offset = 0
limit = 50
if args.offset:
    offset = args.offset
if args.limit:
    if args.limit > 200:
        print(serror("Error: tracks limit limited to 200 tracks.."))
        exit(2)
    limit = args.limit

try:
    sclient = sclient(args.client_id)
    suser = suser(args.user, client=sclient)
except serror as e:
    print(e)
    exit(3)

tracks_getter = suser.get_likes
if args.tracks:
    tracks_getter = suser.get_tracks

if args.recursive:
    while True:
        nb = downloader(tracks_getter, args.output_dir, offset, limit)
        if nb == 0:
            break

        offset = offset + limit
else:
    downloader(tracks_getter, args.output_dir, offset, limit)
