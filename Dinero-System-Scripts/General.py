import urllib2
import urllib
import json

url = "https://www.google.com/?gfe_rd=cr&ei=P9MhV63HHvHR8gfOgpSQAQ&gws_rd=cr&fg=1#q="

query = raw_input("What do you want to search for ? >> ")

query = urllib.urlencode( {'q' : query } )

response = urllib2.urlopen (url + query ).read()

data = json.loads ( response )

results = data [ 'responseData' ] [ 'results' ]

for result in results:
    title = result['title']
    url = result['url']
    print ( title + '; ' + url )