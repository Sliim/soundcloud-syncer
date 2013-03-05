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
# You should have received a copy of the GNU General Public License along
# with Soundcloud-syncer. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import argparse
import os.path

from ssyncer.sclient import sclient
from ssyncer.suser import suser
from ssyncer.serror import serror

parser = argparse.ArgumentParser(description="Soundcloud Syncer")
parser.add_argument("-u", "--user", help="Soundcloud user to sync", type=str, required=True)
parser.add_argument("-c", "--client-id", help="Your client id", type=str, required=False)
parser.add_argument("-o", "--output-dir", help="Output directory", type=str, required=True)
parser.add_argument("-O", "--offset", help="Tracks offset", type=int, required=False)
parser.add_argument("-L", "--limit", help="Tracks limit (max: 200)", type=int, required=False)
args = parser.parse_args()

if not os.path.exists(args.output_dir):
    print("Error: output directory `%s` doesn's exists." % args.output_dir)
    exit(1)

offset = 0
limit = 50
if args.offset:
    offset = args.offset
if args.limit:
    limit = args.limit

try:
    sclient = sclient(args.client_id)
    suser = suser(args.user, client=sclient)
    likes = suser.get_likes(offset, limit)
except serror as e:
    print(e)
    exit(2)

for strack in likes:
    print("Start downloading %s (%s).." % (strack.get("title"), strack.get("id")))
    try:
        strack.download(args.output_dir)
    except serror as e:
        print(e)
