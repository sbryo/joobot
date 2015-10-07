#!/usr/bin/env python2.7
 
# get_links.py
 

import exceptions
import re
import sys
import urllib
import urllib2 
import urlparse
from BeautifulSoup import BeautifulSoup
 
class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
 
def process(url):
    list = []
    #if "bing" in url:
    #	return()
    myopener = MyOpener()
    #page = urllib.urlopen(url)
    page = myopener.open(url)
 
    text = page.read()
    page.close()
 
    soup = BeautifulSoup(text)
    file = open("users-folders/shaked/Results.txt","w")
    file2 = open("users-folders/shaked/History.txt","a")
    for tag in soup.findAll('a', href=True):
   	tag['href'] = urlparse.urljoin(url, tag['href'])
	if "bing" not  in tag['href']:
		if "microsoft" not in tag['href']:
			if "javascript" not in tag['href']:
				#if tag['href'] not in open("/app/users-folders/shaked/my-news").read():
				try:
						#print tag['href'].title()
					LINK_FOR_FILE = str(tag['href'] + '\n')
					#TITLE = tag.find('title')	
					PAGE = myopener.open(tag['href'])
						#TEXT = PAGE.read()
						#PAGE.close()
					try:
							#print PAGE.read().split('<title>')[1].split('</title>')[0].strip()
						TITLE = str(PAGE.read().split('<title>')[1].split('</title>')[0].strip())
						#print TITLE
					except IndexError:
						print "Exception!"
				#file.write((tag['href']+'\n').encode("utf-8"))
				#file.write(LINK_FOR_FILE.decode())
				#file.write(tag['href'].encode('utf-8') + '\n
					file.write((TITLE+' = '+LINK_FOR_FILE).decode("utf-8"))
					file2.write((TITLE+' = '+LINK_FOR_FILE).decode("utf-8"))
				except UnicodeEncodeError:
					continue
    file.close()
    file2.close()
# process(url)
 
def main():
    if len(sys.argv) == 1:
        print "Jabba's Link Extractor v0.1"
        print "Usage: %s URL [URL]..." % sys.argv[0]
        sys.exit(-1)
    # else, if at least one parameter was passed
    for url in sys.argv[1:]:
	#if "bing" not in url:
	process(url)
# main()
 
if __name__ == "__main__":
    main()
