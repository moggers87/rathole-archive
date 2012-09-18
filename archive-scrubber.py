import xml.etree.ElementTree as etree
# archive starts page 1

archive = "http://ratholeradio.org/feed/podcast/?format=ogg&paged=%i"
page_number = 1
page = ""


while 1:
    # get feed at page
    # store page
    feed_tree = etree.fromstring()
    # compare to last page
        # if the same break, we have all the pages
    for item in feed_tree.find("channel").findall("item"):
        item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
