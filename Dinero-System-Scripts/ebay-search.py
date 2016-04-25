#!/usr/bin/python

import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json 

#api connection:
api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None)
#response details:
response = api.execute('findItemsAdvanced',{'keywords':'Woman Bag'})
assert(response.reply.ack == 'Success')
#from today:
#assert(type(response.reply.timestamp) == datetime.datetime)
#get the list:
assert(type(response.reply.searchResult.item) == list)
#item = response.reply.searchResult.item[0]
for item in response.reply.searchResult.item:
	print item

	#item=json.loads(str(item))
	#print item['title']


