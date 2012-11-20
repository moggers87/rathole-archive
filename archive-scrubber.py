# -*- coding: utf-8 -*-
import time, re, urllib2, json
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as etree

archive = ["http://ratholeradio.org/category/podcast/feed/?paged=%i","http://ratholeradio.org/category/uncategorized/feed/?paged=%i","http://ratholeradio.org/category/live/feed/?paged=%i","http://ratholeradio.org/category/interview-2/feed/?paged=%i"]

# set regexs outside the loops
track_matching = re.compile("[0-9]{2}\:[0-9]{2}", re.MULTILINE) # find things like 12:45
detail_matching = re.compile("&#8211;|&#8212;|-", re.MULTILINE) # split out dashes

database_file = 'database.json'

try:
    database = open(database_file, 'r')
    episodes = json.load(database, 'utf-8')
except Exception, e:
    print e
    episodes = {}

def get_tracks(found_tags):
    """Pick out timestamps for songs and parse strings as best we can"""
    tracks = {}
    for tag in found_tags:
        # each time stamp doesn't occur with a <p> or a <li> :(
        times = track_matching.findall(tag.getText())
        details = track_matching.split(tag.getText())[-len(times):]
        i = 0
        while i < len(times):
            track_info = detail_matching.split(details[i])[1:]
            if not len(track_info):
                i = i + 1
            elif u'LIVE SONG' in track_info[0]:
                i = i + 1
            else:
                tracks[times[i]] = track_info[:2]
                i = i + 1
    return tracks

for url in archive:
    page_number = 1

    while 1:
        try:
            # Grab a page
            feed = urllib2.urlopen(url % page_number).read() 
            feed_tree = etree.fromstring(feed)
            page_number = page_number + 1
        except urllib2.HTTPError:
            print "No more pages on %s" % url
            break
        
        """# local 'feed' for debugging
        feed = open('rss-example.xml').read()
        feed_tree = etree.fromstring(feed)
        """
        # Parse xml from feed
        for item in feed_tree.find('channel').findall('item'):
            link = item.find('link').text

            # Test to see if we already have this show or not
            try:
                episodes[link]
                continue
            except KeyError:
                print "We've not seen %s yet" % link

            # Grab tracks
            html = BeautifulSoup(item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)
            tracks = get_tracks(html.findAll('p'))
            tracks.update(get_tracks(html.findAll('li')))
            episodes[link] = tracks

database = open(database_file, 'w')
database.write(json.dumps(episodes, sort_keys=True, indent=4))
database.close()
