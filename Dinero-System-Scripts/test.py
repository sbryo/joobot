from pygoogle import pygoogle
import lxml.html
import urllib

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'


RESULTS_FILE = open("../users-folders/shaked/Results.txt",'a')
HISTORY_FILE = open("../users-folders/shaked/History.txt",'a')


g = pygoogle('woman bag')
g.pages = 10
print '*Found %s results*'%(g.get_result_count())
list=g.get_urls()

for URL in list:
    print URL

for URL in list:
        t = lxml.html.parse(URL)
        print t.find(".//title").text
        PAGE = urllib.urlopen(URL)
        TITLE = str(PAGE.read().split('<title>')[1].split('</title>')[0].strip())
        print TITLE
        print URL
        RESULTS_FILE.write(TITLE+" = "+URL+'\n')
        HISTORY_FILE.write(TITLE+" = "+URL+'\n')


RESULTS_FILE.close()
HISTORY_FILE.close()

