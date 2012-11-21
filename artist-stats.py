# -*- coding: utf-8 -*-
import json

database_file = 'database.json'
database = json.load(open(database_file, 'r'), 'utf-8')

artists = {}

for title, episode in database.iteritems():
    for time, track in episode.iteritems():
        artist = track[0].strip()
        if artist in artists:
            artists[artist] = artists[artist] + 1
        else:
            artists[artist] = 1

count = {count:artist for artist, count in artists.items()}
print "Most played artist: %s" % count[count.keys()[-1]]
