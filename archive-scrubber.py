import time, re
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as etree
# archive starts page 1

archive = "http://ratholeradio.org/feed/podcast/?format=ogg&paged=%i"
page_number = 1
page = ''


while 1:
    # get feed at page
    # store page

    #pretend feed:
    feed = open('rss-example.xml').read()
    
    feed_tree = etree.fromstring(feed)
    # compare to last page
        # if the same break, we have all the pages

    #set regexs outside the loops
    track_matching = re.compile("[0-9]{2}\:[0-9]{2}", re.MULTILINE)
    detail_matching = re.compile("&#8211;|&#8212;", re.MULTILINE)

    # Parse xml from feed
    for item in feed_tree.find('channel').findall('item'):
        html = BeautifulSoup(item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)
        print detail_matching.split(item.find('title').text.encode('utf-8'))[0]

        for p in html.findAll('p'):
            # pick out timestamps for songs and parse strings
            # each time stamp doesn't occur with a <p> :(
            times = track_matching.findall(p.getText())
            details = track_matching.split(p.getText())[-len(times):]
            i = 0
            while i < len(times):
                track_info = detail_matching.split(details[i])[1:]
                if not len(track_info):
                    i = i + 1
                elif u'LIVE SONG' in track_info[0]:
                    i = i + 1
                else:
                    print "%s: %s" % (times[i], track_info)
                    i = i + 1
    break
