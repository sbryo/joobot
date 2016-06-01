import os

import requests
from BeautifulSoup import BeautifulSoup

#URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A3%2F1%2F13%2Ccd_max%3A3%2F2%2F13&as_nsrc=Gulf%20Times&authuser=0'

#URL = 'http://www.bing.com/news/search?q={query}&qft=interval%3d%227%22&form=PTFTNR'
URL = 'http://www.bing.com/search?q={query}'

def run(**params):
    response = requests.get(URL.format(**params))
    #print response.content, response.status_code
    print (response.url)
    page = requests.get(response.url)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    #print (response.status_code)
    #print (response.content)
    os.system("python get_links.py "+response.url)
    

file = open("../users-folders/shaked/SearchFile.txt",'r')
lines = file.readlines()

#run(query="ximena navarrete", month=11, from_day=7, to_day=8, year=14)
for line in lines:
	split = line.split(';')
	line = split[0]
	run(query=line)
