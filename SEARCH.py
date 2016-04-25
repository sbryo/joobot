#!/usr/bin/env python2.7

import os
import urllib

from pygoogle import pygoogle


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'


# GET THE INPUT FROM THE WEB (THE FILE OF THE USER THAT GET INPUT FROM WEB #
FILE = open('users-folders/shaked/SearchFile.txt','r')
LINES = FILE.readlines()
LINE = LINES[0]
SPLIT = LINE.split(';')
PRODUCT = SPLIT[0]
WEBS = SPLIT[1].split(',')
FILE.close()
LIST2 = []
#os.system("echo > users-folders/shaked/Results.txt")

RESULTS_FILE = open("users-folders/shaked/Results.txt",'a')
HISTORY_FILE = open("users-folders/shaked/History.txt",'a')

for WEB in WEBS:
	print WEB
	# SEARCH AND GET URLs	
	G = pygoogle(PRODUCT+" "+WEB,pages=5)
	URLS_LIST = G.get_urls()
	for i in URLS_LIST:
		print i
		#URL= i.split("'")[1]
		URL=i
		for WEB in WEBS:
			if WEB in URL:
		# read source page and get title like the old script "get_links.py" #
				PAGE = myopener.open(URL)
				TITLE = str(PAGE.read().split('<title>')[1].split('</title>')[0].strip())
		# WRITE THE RESULTS TO FILE
				print TITLE
				print URL
				RESULTS_FILE.write(TITLE+" = "+URL+'\n')
				HISTORY_FILE.write(TITLE+" = "+URL+'\n')
RESULTS_FILE.close()
HISTORY_FILE.close()
    	
