#!/usr/bin/python2.6

from pygoogle import pygoogle 

SEARCH_FILE = open("users-folders/shaked/SearchFile.txt","r")
LINES = SEARCH_FILE.readlines()
LINE = LINES[0]
PRODUCT = (LINE.split(';'))[0]
WEBS = (LINE.split(';'))[1]


for WEB in WEBS:
	G = pygoogle(PRODUCT)
	G.pages = 5
	G.get_result_count()
	G.get_urls()



