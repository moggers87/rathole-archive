import time
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

    # Parse xml from feed
    for item in feed_tree.find('channel').findall('item'):
        html = BeautifulSoup(item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)
        for p in html.findAll('p'):
            # pick out timestamps for songs and parse strings
            # each time stamp doesn't occur with a <p> :(
            print p.getText()
            print "====="
        break
    break
