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

import json

json_bytes = b'''[{
    "downloadable": true,
    "id": 1337,
    "kind": "track",
    "original_format": "mp3",
    "permalink": "foo",
    "title": "Foo",
    "user": {
        "permalink": "user1",
        "permalink_url": "http://user1.dev",
        "username": "User 1"
    },
    "created_at": "2013/12/18 13:37:00 +0000",
    "duration": "247010",
    "original_content_size": "9931892",
    "tags_list": "dubstep bass",
    "genre":"Dubstep",
    "description":"Some text",
    "license":"free",
    "uri":"https://api.foobar.dev/1337",
    "permalink_url":"https://foobar.dev/1337",
    "artwork_url":"https://foobar.dev/1337-large.jpg"
}, {
    "downloadable": false,
    "id": 1338,
    "kind": "track",
    "original_format": "mp3",
    "permalink": "bar",
    "title": "Bar",
    "user": {
        "permalink": "user2",
        "permalink_url": "http://user2.dev",
        "username": "User 2"
    },
    "created_at": "2013/12/18 13:37:01 +0000",
    "duration": "247011",
    "original_content_size": "9931893",
    "tags_list": "trap bass",
    "genre":"Trap",
    "description":"Some description",
    "license":"Common",
    "uri":"https://api.foobar.dev/1338",
    "permalink_url":"https://foobar.dev/1338",
    "artwork_url":"https://foobar.dev/1338-large.jpg"
}, {
    "downloadable": true,
    "id": 1339,
    "kind": "track",
    "original_format": "wav",
    "permalink": "baz",
    "title": "Baz",
    "user": {
        "permalink": "user3",
        "permalink_url": "http://user3.dev",
        "username": "User 3"
    },
    "created_at": "2013/12/18 13:37:02 +0000",
    "duration": "247012",
    "original_content_size": "9931894",
    "tags_list": "drumandbass bass",
    "genre":"D&B",
    "description":"Awesome D&B",
    "license":"copyleft",
    "uri":"https://api.foobar.dev/1339",
    "permalink_url":"https://foobar.dev/1339",
    "artwork_url":"https://foobar.dev/1339-large.jpg"
}
]'''
playlists_bytes = b'''[{
    "duration":2524859,
    "release_day":"Monday",
    "permalink_url":"http://soundcloud.com/5liim/sets/dabass",
    "reposts_count":0,
    "genre":"dnb",
    "permalink":"dabass",
    "purchase_url":null,
    "release_month":"February",
    "description":"My awesome playlist",
    "uri":"https://api.soundcloud.com/playlists/1337",
    "label_name":"My Playlist",
    "tag_list":"awesome",
    "release_year":2020,
    "track_count":42,
    "user_id":1337,
    "last_modified":"2015/04/22 08:13:52 +0000",
    "license":"Beerware",
    "tracks":[]}
]'''

json_obj = json.loads(json_bytes.decode("utf-8"))
playlists_obj = json.loads(playlists_bytes.decode("utf-8"))
